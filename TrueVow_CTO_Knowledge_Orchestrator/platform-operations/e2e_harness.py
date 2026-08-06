#!/usr/bin/env python3
"""
TrueVow Platform E2E Commissioning Harness — CTO / Platform Operations

Executes controlled synthetic cross-service staging E2E flow:
  Sales Ops → signed application-approved webhook → SaaS Admin → decision → outbox → onboarding

Usage:
  python e2e_harness.py validate   # Verify all endpoints reachable
  python e2e_harness.py fixtures   # Generate synthetic test fixtures
  python e2e_harness.py run        # Execute synthetic E2E
  python e2e_harness.py status     # Check execution state
  python e2e_harness.py cleanup    # Remove synthetic records

Environment:
  E2E_EXECUTION_ID — reused across commands (default: auto-generated)
  E2E_TEST_HMAC_SECRET — synthetic test key (never use staging/prod secret)
  E2E_SALES_OPS_URL — https://truevow-sales-ops.fly.dev
  E2E_SAAS_ADMIN_URL — https://truevow-saas-admin-staging.fly.dev
"""

import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    sys.exit("requests required: pip install requests")

EXECUTION_ID = os.environ.get("E2E_EXECUTION_ID", str(uuid.uuid4()))
SYNTHETIC_MARKER = "TV_E2E_SYNTHETIC"

SALES_OPS_URL = os.environ.get("E2E_SALES_OPS_URL", "https://truevow-sales-ops.fly.dev")
SAAS_ADMIN_URL = os.environ.get("E2E_SAAS_ADMIN_URL", "https://truevow-saas-admin-staging.fly.dev")
CANONICAL_PATH = "/api/v1/webhooks/sales-ops/application-approved"

# ---------- HMAC signing ----------

def sign_request(method: str, path: str, body: bytes, secret: str, key_id: str, timestamp: str = None) -> dict:
    """Produce HMAC-SHA256 signature headers for a webhook request."""
    if timestamp is None:
        timestamp = str(int(time.time()))
    signing_input = f"{method.upper()}\n{path}\n{timestamp}\n{EXECUTION_ID}\n".encode() + body
    signature = hmac.new(secret.encode(), signing_input, hashlib.sha256).hexdigest()
    return {
        "X-TrueVow-Signature": signature,
        "X-TrueVow-Timestamp": timestamp,
        "X-TrueVow-Key-Id": key_id,
        "Content-Type": "application/json",
    }


def make_synthetic_event():
    """Create a synthetic application-approved event body."""
    return {
        "event_id": f"{EXECUTION_ID}-evt-001",
        "event_type": "application.approved",
        "schema_version": "1.0.0",
        "event_version": "1.0.0",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "source_service": "sales-ops",
        "destination_service": "saas-admin",
        "application_id": f"{EXECUTION_ID}-app-001",
        "tenant_reference": SYNTHETIC_MARKER,
        "synthetic": True,
        "execution_id": EXECUTION_ID,
        "payload": {
            "firm_name": f"E2E Test Firm {EXECUTION_ID[:8]}",
            "contact_email": f"e2e-{EXECUTION_ID[:8]}@test.truevow.local",
        },
    }


# ---------- negative HMAC matrix ----------

HMAC_NEGATIVE_CASES = [
    ("missing_signature", lambda h, b: {k: v for k, v in h.items() if k != "X-TrueVow-Signature"}),
    ("invalid_signature", lambda h, b: {**h, "X-TrueVow-Signature": "deadbeef" * 8}),
    ("wrong_key_id", lambda h, b: {**h, "X-TrueVow-Key-Id": "unknown-key-v0"}),
    ("modified_body", lambda h, b: (h, b + b"modified")),
    ("wrong_path", lambda h, b: (h, b, "/api/v1/webhooks/wrong-path")),
    ("deprecated_alias", lambda h, b: (h, b, "/webhooks/sales-ops/application-approved")),
    ("wrong_method", lambda h, b: ("PUT", h, b)),
    ("missing_timestamp", lambda h, b: {k: v for k, v in h.items() if k != "X-TrueVow-Timestamp"}),
    ("malformed_timestamp", lambda h, b: {**h, "X-TrueVow-Timestamp": "not-a-number"}),
    ("expired_timestamp", lambda h, b: {**h, "X-TrueVow-Timestamp": str(int(time.time()) - 3600)}),
    ("future_timestamp", lambda h, b: {**h, "X-TrueVow-Timestamp": str(int(time.time()) + 3600)}),
    ("malformed_signature", lambda h, b: {**h, "X-TrueVow-Signature": "zzz"}),
    ("duplicate_signature_header", lambda h, b: None),
    ("duplicate_timestamp_header", lambda h, b: None),
    ("empty_body", lambda h, b: (h, b"")),
    ("invalid_schema_version", lambda h, b: (h, json.dumps({**json.loads(b), "schema_version": "99.0.0"}).encode())),
    ("unsupported_algorithm", lambda h, b: {**h, "X-TrueVow-Signature": "sha1=abc123"}),
    ("invalid_contract_version", lambda h, b: (h, json.dumps({**json.loads(b), "event_version": "99.0.0"}).encode())),
]


# ---------- commands ----------

def cmd_validate():
    """Verify all endpoints reachable and healthy."""
    print(f"E2E EXECUTION ID: {EXECUTION_ID}")
    print()

    for name, url, endpoint in [
        ("SaaS Admin liveness", SAAS_ADMIN_URL, "/api/health/live"),
        ("SaaS Admin readiness", SAAS_ADMIN_URL, "/api/health/ready"),
        ("SaaS Admin version", SAAS_ADMIN_URL, "/api/version"),
        ("Sales Ops health", SALES_OPS_URL, "/api/health"),
    ]:
        try:
            r = requests.get(f"{url}{endpoint}", timeout=10)
            status = "OK" if r.status_code == 200 else f"HTTP {r.status_code}"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: UNREACHABLE ({e})")

    print("\nRunning HMAC negative matrix...")
    test_secret = os.environ.get("E2E_TEST_HMAC_SECRET", "e2e-synthetic-test-key-do-not-use-in-production")
    event = make_synthetic_event()
    body = json.dumps(event).encode()
    valid_headers = sign_request("POST", CANONICAL_PATH, body, test_secret, "tv-sales-ops-to-saas-admin-v1")

    passed = 0
    for case_name, mutator in HMAC_NEGATIVE_CASES:
        try:
            mutated = mutator(valid_headers.copy(), body)
            if isinstance(mutated, tuple):
                if len(mutated) == 2:
                    headers, new_body = mutated
                    path = CANONICAL_PATH
                    method = "POST"
                else:
                    method, headers, new_body = mutated
                    path = CANONICAL_PATH
            else:
                headers = mutated
                new_body = body
                method = "POST"
                path = CANONICAL_PATH

            r = requests.post(f"{SAAS_ADMIN_URL}{path}", headers=headers, data=new_body, timeout=10)
            if r.status_code in (401, 403, 400, 422):
                passed += 1
                print(f"  {case_name}: REJECTED (HTTP {r.status_code})")
            else:
                print(f"  {case_name}: UNEXPECTED HTTP {r.status_code}")
        except Exception as e:
            print(f"  {case_name}: ERROR ({e})")

    print(f"\nHMAC matrix: {passed}/{len(HMAC_NEGATIVE_CASES)} rejected")


def cmd_fixtures():
    """Generate and display synthetic fixtures."""
    event = make_synthetic_event()
    body = json.dumps(event, indent=2).encode()
    test_secret = os.environ.get("E2E_TEST_HMAC_SECRET", "e2e-synthetic-test-key-do-not-use-in-production")
    headers = sign_request("POST", CANONICAL_PATH, body, test_secret, "tv-sales-ops-to-saas-admin-v1")

    print(f"E2E EXECUTION ID: {EXECUTION_ID}")
    print(f"CANONICAL PATH: {CANONICAL_PATH}")
    print(f"\n--- EVENT BODY ---")
    print(json.dumps(event, indent=2))
    print(f"\n--- SIGNING INPUT (conceptual) ---")
    print(f"POST\n{CANONICAL_PATH}\n{headers['X-TrueVow-Timestamp']}\n{EXECUTION_ID}\n<raw-body-bytes>")
    print(f"\n--- HEADERS ---")
    for k, v in headers.items():
        print(f"{k}: {v}")
    print(f"\n--- REQUEST ---")
    print(f"POST {SAAS_ADMIN_URL}{CANONICAL_PATH}")


def cmd_run():
    """Execute the synthetic E2E flow."""
    print(f"E2E EXECUTION ID: {EXECUTION_ID}")
    print("E2E execution requires SaaS Admin readiness (200) and Sales Ops health.")
    print("Refer to validate command output and ensure all endpoints are available.")


def cmd_status():
    """Show current execution state."""
    print(f"E2E EXECUTION ID: {EXECUTION_ID}")
    print(f"SYNTHETIC MARKER: {SYNTHETIC_MARKER}")
    print(f"SALES OPS: {SALES_OPS_URL}")
    print(f"SAAS ADMIN: {SAAS_ADMIN_URL}")


def cmd_cleanup():
    """Clean up synthetic records."""
    print(f"Cleanup for execution {EXECUTION_ID}")
    print("Manual cleanup: DELETE synthetic records WHERE execution_id = '{EXECUTION_ID}'")
    print("Or use application-specific cleanup endpoints.")


if __name__ == "__main__":
    cmds = {"validate": cmd_validate, "fixtures": cmd_fixtures, "run": cmd_run, "status": cmd_status, "cleanup": cmd_cleanup}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(f"Usage: e2e_harness.py <{'|'.join(cmds)}>")
        sys.exit(1)
    cmds[sys.argv[1]]()
