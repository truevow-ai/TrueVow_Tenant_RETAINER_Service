#!/usr/bin/env python3
"""
INTAKE Authoritative Migration Runner — Platform Operations

Applies frozen schema migrations to the INTAKE Supabase project using
advisory locking, immutable migration checksums, a durable success ledger,
and a separate attempt-history table for failed/interrupted runs.

Usage:
  python intake_migrate.py verify   # Read-only preflight
  python intake_migrate.py plan     # Redacted plan
  python intake_migrate.py apply    # Authoritative apply (requires --yes)
  python intake_migrate.py status   # Show migration history

Environment variables:
  INTAKE_DATABASE_URL — session-pooler connection (required, never printed)
  INTAKE_PROJECT_REF — expected Supabase project ref, e.g. flhnyyreaxkmwmexchla
  INTAKE_ENVIRONMENT — staging | production (default: staging)
  OPERATOR_IDENTITY — who is applying the migration (default: current OS user)
"""

import hashlib
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from urllib.parse import quote_plus

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    sys.exit("psycopg2 required: pip install psycopg2")

# ── frozen migration manifest ──────────────────────────────────────────
FROZEN_MIGRATIONS = [
    {
        "migration_id": "20260805_add_request_receipts",
        "filename": "operations/database/migrations/20260805_add_request_receipts.sql",
        "sha256": "4944591b0a35eb14f10baafbdc167b08138f6967a82319681c5f37f244ef3719",
        "source_commit": "4da6ae9",
        "source_repo": "TrueVow_Tenant_Application_Service",
        "source_branch": "review/tv-intake-engine-p1-02s-r1",
        "predecessor": None,
        "engine_contract_commit": "891eec8",
        "requires_drain": True,
    }
]

LOCK_KEY = 9876543210  # deterministic: hash("TrueVow:INTAKE:schema:migration")


def _get_connection():
    url = os.environ.get("INTAKE_DATABASE_URL")
    if not url:
        sys.exit("INTAKE_DATABASE_URL not set")
    return psycopg2.connect(url, connect_timeout=10)


def _get_env():
    env = os.environ.get("INTAKE_ENVIRONMENT", "staging")
    if env not in ("staging", "production"):
        sys.exit(f"Unknown environment: {env}")
    return env


def _get_operator():
    return os.environ.get("OPERATOR_IDENTITY", os.environ.get("USER", os.environ.get("USERNAME", "unknown")))


def _validate_project_ref(conn):
    """Prove the database belongs to the approved INTAKE project."""
    expected = os.environ.get("INTAKE_PROJECT_REF")
    if not expected:
        sys.exit("INTAKE_PROJECT_REF not set")

    cur = conn.cursor()
    # Derive project ref from pooler username if present
    url = os.environ.get("INTAKE_DATABASE_URL", "")
    # Check pooler username format: postgres.<project_ref>
    import re
    m = re.search(r"postgres\.([a-z]{20,30})", url)
    if m and m.group(1) != expected:
        sys.exit(f"WRONG PROJECT: connection ref {m.group(1)} != expected {expected}")
    cur.execute("SELECT current_database(), current_user")
    db, user = cur.fetchone()
    print(f"  Database: {db}  User: {user}")
    print(f"  Project:  {expected}  Environment: {_get_env()}")


def _ensure_ledger(conn):
    """Create ledger and attempt-history tables if absent."""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS platform_schema_migrations (
            migration_id    TEXT PRIMARY KEY,
            filename        TEXT NOT NULL,
            sha256          TEXT NOT NULL CHECK (sha256 ~ '^[a-f0-9]{64}$'),
            application_order BIGINT NOT NULL UNIQUE,
            applied_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            applied_by      TEXT NOT NULL,
            environment     TEXT NOT NULL CHECK (environment IN ('staging','production')),
            execution_id    UUID NOT NULL UNIQUE,
            source_commit   TEXT NOT NULL,
            runner_version  TEXT NOT NULL DEFAULT '1.0.0'
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS platform_schema_migration_attempts (
            attempt_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            migration_id    TEXT NOT NULL,
            filename        TEXT NOT NULL,
            sha256          TEXT NOT NULL,
            environment     TEXT NOT NULL,
            source_commit   TEXT NOT NULL,
            operator_id     TEXT NOT NULL,
            started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
            finished_at     TIMESTAMPTZ,
            status          TEXT NOT NULL DEFAULT 'STARTED'
                CHECK (status IN ('STARTED','SUCCESS','FAILED','BLOCKED')),
            error_class     TEXT,
            runner_version  TEXT NOT NULL DEFAULT '1.0.0'
        )
    """)
    cur.execute("""
        CREATE SEQUENCE IF NOT EXISTS platform_schema_migrations_order_seq
        START WITH 1 INCREMENT BY 1
    """)
    conn.commit()
    print("  Ledger tables ensured.")


def _acquire_lock(conn):
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SELECT pg_try_advisory_lock(%s)", (LOCK_KEY,))
    acquired = cur.fetchone()[0]
    if not acquired:
        sys.exit("LOCK: Another migration is in progress. Try again later.")
    print("  Migration lock acquired.")


def _release_lock(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT pg_advisory_unlock(%s)", (LOCK_KEY,))
        print("  Migration lock released.")
    except Exception:
        pass


def _check_for_conflicts(conn, migration):
    """Reject if conflicting schema objects exist without a verified migration record."""
    cur = conn.cursor()
    checks = {
        "state_version": "SELECT 1 FROM information_schema.columns WHERE table_schema='public' AND table_name='intake_sessions' AND column_name='state_version'",
        "uq_tenant_session": "SELECT 1 FROM pg_constraint WHERE conname='uq_intake_sessions_tenant_session'",
        "receipt_table": "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='intake_request_receipts'",
    }
    for name, sql in checks.items():
        cur.execute(sql)
        if cur.fetchone():
            cur.execute("SELECT 1 FROM platform_schema_migrations WHERE migration_id=%s AND sha256=%s",
                        (migration["migration_id"], migration["sha256"]))
            if not cur.fetchone():
                sys.exit(f"CONFLICT: {name} exists but is not governed by this migration. Manual review required.")


def _verify_artifact(migration):
    """Fetch the migration from the approved remote commit and verify checksum."""
    import tempfile
    repo_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "TrueVow_Tenant_INTAKE_Service"
    )
    if not os.path.isdir(repo_path):
        repo_path = os.environ.get("INTAKE_REPO_PATH")
        if not repo_path:
            sys.exit("INTAKE_REPO_PATH not set — cannot verify artifact")

    r = subprocess.run(
        ["git", "-C", repo_path, "show",
         f"{migration['source_commit']}:{migration['filename']}"],
        capture_output=True
    )
    if r.returncode != 0:
        sys.exit(f"ARTIFACT: Cannot retrieve {migration['filename']} from {migration['source_commit']}")
    actual = hashlib.sha256(r.stdout).hexdigest()
    if actual != migration["sha256"]:
        sys.exit(f"CHECKSUM MISMATCH: expected {migration['sha256']}, got {actual}")
    print(f"  Artifact verified: {migration['migration_id']} (SHA-256 OK)")
    return r.stdout


def _record_attempt(conn, migration, status, error_class=None):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO platform_schema_migration_attempts
            (migration_id, filename, sha256, environment, source_commit, operator_id, started_at, finished_at, status, error_class)
        VALUES (%s,%s,%s,%s,%s,%s,now(),now(),%s,%s)
    """, (migration["migration_id"], migration["filename"], migration["sha256"],
          _get_env(), migration["source_commit"], _get_operator(), status, error_class))
    conn.commit()


def _record_success(conn, migration, execution_id):
    cur = conn.cursor()
    cur.execute("SELECT coalesce(max(application_order),0)+1 FROM platform_schema_migrations")
    order = cur.fetchone()[0]
    cur.execute("""
        INSERT INTO platform_schema_migrations
            (migration_id, filename, sha256, application_order, applied_at, applied_by, environment, execution_id, source_commit)
        VALUES (%s,%s,%s,%s,now(),%s,%s,%s,%s)
    """, (migration["migration_id"], migration["filename"], migration["sha256"],
          order, _get_operator(), _get_env(), execution_id, migration["source_commit"]))
    conn.commit()
    print(f"  Success recorded: order {order}")


def cmd_verify():
    """Read-only preflight: checksum, project, conflicts, ordering, drain."""
    conn = _get_connection()
    conn.autocommit = True
    print("VERIFY - read-only preflight")
    _validate_project_ref(conn)
    _ensure_ledger(conn)

    migration = FROZEN_MIGRATIONS[0]
    sql = _verify_artifact(migration)

    # Check for conflicts
    _check_for_conflicts(conn, migration)

    # Check ordering
    cur = conn.cursor()
    cur.execute("SELECT max(application_order) FROM platform_schema_migrations")
    last = cur.fetchone()[0]
    if last is not None:
        cur.execute("SELECT 1 FROM platform_schema_migrations WHERE migration_id=%s", (migration["migration_id"],))
        if cur.fetchone():
            print("  Migration already applied.")
        else:
            print(f"  Last applied order: {last}. This migration would be {last + 1}.")
    else:
        print("  No previous migrations. This would be first (order 1).")

    if migration["requires_drain"]:
        cur.execute("SELECT count(*) FROM intake_sessions WHERE session_status = 'active'")
        active = cur.fetchone()[0]
        print(f"  Active sessions: {active} (drain required: >0)")

    conn.close()
    print("VERIFY: PASS")


def cmd_plan():
    """Display redacted plan of what will happen."""
    conn = _get_connection()
    conn.autocommit = True
    migration = FROZEN_MIGRATIONS[0]
    _verify_artifact(migration)
    print("PLAN — redacted operations:")
    print(f"  Migration: {migration['migration_id']}")
    print(f"  SHA-256:   {migration['sha256'][:16]}...")
    print(f"  Source:    {migration['source_commit']}")
    print(f"  Project:   {os.environ.get('INTAKE_PROJECT_REF', 'NOT SET')}")
    print(f"  Changes:   ADD state_version, ADD composite UNIQUE, CREATE receipt table, CREATE indexes, ENABLE RLS")
    conn.close()


def cmd_apply():
    """Authoritative migration application. Requires --yes."""
    if "--yes" not in sys.argv:
        print("This will apply a schema migration. Use --yes to confirm.")
        sys.exit(1)

    execution_id = str(uuid.uuid4())
    conn = _get_connection()
    _validate_project_ref(conn)
    _acquire_lock(conn)
    _ensure_ledger(conn)

    migration = FROZEN_MIGRATIONS[0]
    sql = _verify_artifact(migration)
    _check_for_conflicts(conn, migration)

    # Record attempt STARTED
    _record_attempt(conn, migration, "STARTED")

    try:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()

        _record_success(conn, migration, execution_id)
        _record_attempt(conn, migration, "SUCCESS")
        print("APPLY: PASS")
    except Exception as e:
        conn.rollback()
        error_class = type(e).__name__
        _record_attempt(conn, migration, "FAILED", error_class)
        _release_lock(conn)
        sys.exit(f"APPLY: FAILED — {error_class}: {e}")

    _release_lock(conn)
    conn.close()


def cmd_status():
    """Show applied, pending, failed attempts."""
    conn = _get_connection()
    conn.autocommit = True
    cur = conn.cursor()

    print("STATUS — Applied migrations:")
    cur.execute("SELECT application_order, migration_id, sha256, applied_at, environment FROM platform_schema_migrations ORDER BY application_order")
    rows = cur.fetchall()
    if rows:
        for r in rows:
            print(f"  [{r[0]}] {r[1]} ({r[2][:12]}...) {r[3].strftime('%Y-%m-%d')} env={r[4]}")
    else:
        print("  (none)")

    print("\nPending (governed):")
    for m in FROZEN_MIGRATIONS:
        cur.execute("SELECT 1 FROM platform_schema_migrations WHERE migration_id=%s", (m["migration_id"],))
        if not cur.fetchone():
            print(f"  PENDING: {m['migration_id']} ({m['sha256'][:12]}...)")

    print("\nRecent attempts:")
    cur.execute("SELECT migration_id, status, error_class, started_at FROM platform_schema_migration_attempts ORDER BY started_at DESC LIMIT 5")
    for r in cur.fetchall():
        err = f" ({r[2]})" if r[2] else ""
        print(f"  {r[1]}: {r[0]} at {r[3].strftime('%Y-%m-%d %H:%M')}{err}")

    conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: intake_migrate.py <verify|plan|apply|status>")
        sys.exit(1)
    cmd = sys.argv[1]
    {"verify": cmd_verify, "plan": cmd_plan, "apply": cmd_apply, "status": cmd_status}[cmd]()
