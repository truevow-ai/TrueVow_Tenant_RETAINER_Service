# INTAKE Migration Commissioning Runbook

## Authority

Platform Operations only. The Tenant INTAKE application must never auto-apply schema migrations.

## Artifacts

| Item | Value |
|------|-------|
| Migration ID | `20260805_add_request_receipts` |
| Source repository | `TrueVow_Tenant_Application_Service` |
| Source branch | `review/tv-intake-engine-p1-02s-r1` |
| Source commit | `4da6ae9` |
| Migration file | `operations/database/migrations/20260805_add_request_receipts.sql` |
| SHA-256 | `4944591b0a35eb14f10baafbdc167b08138f6967a82319681c5f37f244ef3719` |
| Engine contract | `891eec8` |
| Target project | `flhnyyreaxkmwmexchla` |
| Target environment | staging |

## Preconditions

- [ ] No active contact tasks in progress (drain window)
- [ ] Frozen artifact checksum verified from remote
- [ ] Platform Operations operator authorized
- [ ] INTAKE service health: healthy
- [ ] Database credentials available (not in this document)

## Commissioning Sequence

### 1. Verify (read-only)

```bash
export INTAKE_DATABASE_URL="<session-pooler-url>"
export INTAKE_PROJECT_REF="flhnyyreaxkmwmexchla"
export INTAKE_ENVIRONMENT="staging"

python platform-operations/intake_migrate.py verify
```

Expected: all checks pass, no conflicts, no duplicate sessions.

### 2. Plan

```bash
python platform-operations/intake_migrate.py plan
```

Review the redacted plan. Confirm the listed changes match the governed migration.

### 3. Apply

```bash
python platform-operations/intake_migrate.py apply --yes
```

The runner will:
1. Validate project identity
2. Acquire advisory lock
3. Verify artifact checksum from remote commit
4. Check for conflicting schema
5. Record STARTED attempt
6. Apply migration in single transaction
7. Record SUCCESS in ledger and attempt history
8. Release lock

### 4. Verify post-application

```sql
-- state_version created
SELECT column_name FROM information_schema.columns
WHERE table_schema='public' AND table_name='intake_sessions'
AND column_name='state_version';

-- All sessions initialized to 0
SELECT session_id, state_version FROM intake_sessions;

-- Composite UNIQUE active
SELECT conname FROM pg_constraint
WHERE conname='uq_intake_sessions_tenant_session';

-- Receipt table created
SELECT count(*) FROM intake_request_receipts;

-- RLS enabled
SELECT tablename, rowsecurity FROM pg_tables
WHERE schemaname='public' AND tablename='intake_request_receipts';
```

### 5. Verify service health

```bash
curl https://truevow-tenant-public.fly.dev/health
```

Expected: `{"status":"healthy","database":"connected"}`

## Rollback

Before commit: transaction rollback is automatic.
After commit: use a separately reviewed reverse migration. Never manually delete ledger records or drop populated tables.

## Incident

If application fails: review attempt history, do not re-run without resolving root cause. Escalate to Platform Operations.
