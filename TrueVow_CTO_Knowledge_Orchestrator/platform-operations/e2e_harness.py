#!/usr/bin/env python3
"""
TrueVow Platform E2E Commissioning Harness — CTO / Platform Operations
TV-PR-STAGING-E2E-COMMISSIONING-01R2

Corrected HMAC signing to match WebhookSignature v1.0 (FROZEN).
HandoffPayload schema aligned with SaaS Admin webhook contract.

Usage:
  python e2e_harness.py validate   # Verify endpoints + HMAC negative matrix
  python e2e_harness.py run        # Execute synthetic E2E
  python e2e_harness.py status     # Check execution state
  python e2e_harness.py cleanup    # Remove synthetic records
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

SAAS_ADMIN_URL = os.environ.get("E2E_SAAS_ADMIN_URL", "https://truevow-saas-admin-staging.fly.dev")
CANONICAL_PATH = "/api/v1/webhooks/sales-ops/application-approved"

HMAC_SECRET = os.environ.get("E2E_HMAC_SECRET", "")
HMAC_KEY_ID = "tv-sales-ops-to-saas-admin-v1"

REQUEST_TIMEOUT = 30

# ---------- HMAC signing (WebhookSignature v1.0) ----------

def sign_request(method, path, body_str, secret, key_id, timestamp=None):
    if timestamp is None:
        timestamp = str(int(time.time() * 1000))
    body_hash = hashlib.sha256(body_str.encode()).hexdigest()
    signing_string = f"{timestamp}:{method.upper()}:{path}:{body_hash}"
    signature = hmac.new(secret.encode(), signing_string.encode(), hashlib.sha256).hexdigest()
    return {
        "X-TrueVow-Key-Id": key_id,
        "X-TrueVow-Timestamp": timestamp,
        "X-TrueVow-Signature": signature,
        "Content-Type": "application/json",
    }


def js_json_dumps(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=True)


def make_handoff_payload(suffix=""):
    hid = f"{EXECUTION_ID}-h-{uuid.uuid4().hex[:12]}{suffix}"
    payload = {
        "handoff_id": hid,
        "handoff_version": "1.0.0",
        "event_envelope_version": "1.0.1",
        "firm": {"legal_name": f"E2E Test Firm {EXECUTION_ID[:8]}"},
        "primary_contact": {
            "full_name": "Synthetic Partner",
            "email": f"e2e-{EXECUTION_ID[:8]}@test.truevow.local",
            "phone": "+13105559999",
            "title": "Managing Partner",
        },
        "approved_products": [{"product_code": "INTAKE", "tier": "standard", "addons": []}],
        "approval": {
            "approved_by": "CTO Platform Ops",
            "approved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "decision": "approved",
            "authority_ref": "sales-ops-approved",
        },
        "provenance": {
            "lead_id": f"lead-{EXECUTION_ID[:8]}",
            "source_service": "sales-ops",
            "campaign_id": "e2e-harness",
            "cohort_tier": "confirmed_match",
        },
        "sensitivity": "internal",
        "policy_version": "1.0.0",
    }
    payload_for_checksum = {k: v for k, v in payload.items()}
    payload["checksum"] = hashlib.sha256(js_json_dumps(payload_for_checksum).encode()).hexdigest()
    return hid, payload


# ---------- commands ----------

def cmd_validate():
    print(f"E2E EXECUTION ID: {EXECUTION_ID}")
    print()

    if not HMAC_SECRET:
        print("  FATAL: E2E_HMAC_SECRET not set. Cannot run HMAC tests.")

    # Health checks
    checks = [
        ("SaaS Admin version", "/api/version", False),
        ("SaaS Admin liveness", "/api/health/live", False),
        ("SaaS Admin readiness", "/api/health/ready", False),
    ]
    for name, endpoint, _ in checks:
        try:
            r = requests.get(f"{SAAS_ADMIN_URL}{endpoint}", timeout=10)
            status = f"HTTP {r.status_code}"
            if r.status_code == 200:
                status = "OK"
                body = r.json()
                if "build_commit" in body:
                    status += f"  commit={body['build_commit'][:30]}"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: UNREACHABLE ({e})")

    if not HMAC_SECRET:
        return

    print(f"\nRunning HMAC negative matrix ({SAAS_ADMIN_URL[len('https://'):]}{CANONICAL_PATH})...")

    _, event = make_handoff_payload()
    body_str = js_json_dumps(event)
    body_bytes = body_str.encode()
    valid_headers = sign_request("POST", CANONICAL_PATH, body_str, HMAC_SECRET, HMAC_KEY_ID)

    # Valid case first
    try:
        r = requests.post(f"{SAAS_ADMIN_URL}{CANONICAL_PATH}", headers=valid_headers,
                          data=body_bytes, timeout=REQUEST_TIMEOUT)
        if r.status_code == 201:
            print(f"  VALID: HTTP 201 (ACCEPTED)")
        elif r.status_code == 200:
            print(f"  VALID: HTTP 200 (REPLAY — idempotent)")
        else:
            print(f"  VALID: HTTP {r.status_code} (unexpected)")
    except Exception as e:
        print(f"  VALID: ERROR ({e})")

    # Negative cases
    cases = [
        ("missing_signature", lambda h, b: (
            {k: v for k, v in h.items() if k != "X-TrueVow-Signature"}, b)),
        ("invalid_signature", lambda h, b: (
            {**h, "X-TrueVow-Signature": "deadbeef" * 8}, b)),
        ("wrong_key_id", lambda h, b: (
            {**h, "X-TrueVow-Key-Id": "unknown-key-v0"}, b)),
        ("modified_body", lambda h, b: (h, b + b"modified")),
        ("wrong_path", lambda h, b: (h, b, "/api/v1/webhooks/wrong-path")),
        ("deprecated_alias", lambda h, b: (h, b, "/webhooks/sales-ops/application-approved")),
        ("wrong_method", lambda h, b: (h, b, CANONICAL_PATH, "PUT")),
        ("missing_timestamp", lambda h, b: (
            {k: v for k, v in h.items() if k != "X-TrueVow-Timestamp"}, b)),
        ("malformed_timestamp", lambda h, b: (
            {**h, "X-TrueVow-Timestamp": "not-a-number"}, b)),
        ("expired_timestamp", lambda h, b: (
            {**h, "X-TrueVow-Timestamp": str(int(time.time() * 1000) - 3600_000)}, b)),
        ("future_timestamp", lambda h, b: (
            {**h, "X-TrueVow-Timestamp": str(int(time.time() * 1000) + 3600_000)}, b)),
        ("malformed_signature", lambda h, b: (
            {**h, "X-TrueVow-Signature": "zzz"}, b)),
        ("empty_body", lambda h, b: (h, b"")),
        ("invalid_schema_version", lambda h, b: (
            h, js_json_dumps({**json.loads(b), "event_envelope_version": "99.0.0"}).encode())),
        ("unsupported_algorithm", lambda h, b: (
            {**h, "X-TrueVow-Signature": "sha1=abc123"}, b)),
        ("invalid_contract_version", lambda h, b: (
            h, js_json_dumps({**json.loads(b), "handoff_version": "99.0.0"}).encode())),
    ]

    passed = 0
    fail_open = 0

    for case_name, mutator in cases:
        try:
            result = mutator(valid_headers, body_bytes)
            if len(result) == 2:
                hdrs, bdy = result
                path = CANONICAL_PATH
                method = "POST"
            elif len(result) == 3:
                hdrs, bdy, path = result
                method = "POST"
            elif len(result) == 4:
                hdrs, bdy, path, method = result
            else:
                print(f"  {case_name}: SKIP (invalid mutator)")
                continue

            r = requests.request(method, f"{SAAS_ADMIN_URL}{path}",
                                 headers=hdrs, data=bdy, timeout=REQUEST_TIMEOUT)
            if r.status_code in (401, 403, 400, 422):
                passed += 1
                print(f"  {case_name}: REJECTED HTTP {r.status_code}")
            elif r.status_code in (200, 201):
                fail_open += 1
                print(f"  {case_name}: FAIL-OPEN HTTP {r.status_code}")
            else:
                print(f"  {case_name}: HTTP {r.status_code} (non-canonical)")
        except Exception as e:
            print(f"  {case_name}: ERROR ({e})")

    print(f"\nHMAC matrix: {passed}/{len(cases)} rejected, {fail_open} fail-open")


def cmd_run():
    print(f"E2E EXECUTION ID: {EXECUTION_ID}")
    print()

    if not HMAC_SECRET:
        print("  FATAL: E2E_HMAC_SECRET not set.")
        return

    # 1. Fresh handoff
    print("--- Phase 1: Fresh Handoff ---")
    hid, event = make_handoff_payload()
    body_str = js_json_dumps(event)
    body_bytes = body_str.encode()
    headers = sign_request("POST", CANONICAL_PATH, body_str, HMAC_SECRET, HMAC_KEY_ID)

    try:
        r = requests.post(f"{SAAS_ADMIN_URL}{CANONICAL_PATH}", headers=headers,
                          data=body_bytes, timeout=REQUEST_TIMEOUT)
        status = r.status_code
        body = r.json()
        ps = body.get("processing_status", "UNKNOWN")
        tid = body.get("tenant_id", "N/A")
        replay = body.get("idempotent_replay", "N/A")
        slug = body.get("onboarding_reference", "N/A")
        print(f"  Fresh handoff: HTTP {status}  status={ps}  tenant={tid}")
        print(f"  Idempotent replay: {replay}  ref: {slug}")

        if status not in (200, 201):
            print(f"  FAIL: Expected 2xx, got {status}")
            print(f"  Response: {json.dumps(body, indent=2)[:300]}")
            return
    except Exception as e:
        print(f"  FAIL: {e}")
        return

    # 2. Idempotent replay
    print("\n--- Phase 2: Idempotent Replay ---")
    headers2 = sign_request("POST", CANONICAL_PATH, body_str, HMAC_SECRET, HMAC_KEY_ID)
    try:
        r2 = requests.post(f"{SAAS_ADMIN_URL}{CANONICAL_PATH}", headers=headers2,
                           data=body_bytes, timeout=REQUEST_TIMEOUT)
        body2 = r2.json()
        replay2 = body2.get("idempotent_replay", None)
        tid2 = body2.get("tenant_id", "N/A")
        print(f"  Replay: HTTP {r2.status_code}  idempotent_replay={replay2}  tenant={tid2}")
        if replay2 is True and tid2 == tid:
            print("  PASS: Same handoff_id + same checksum -> idempotent replay")
        else:
            print(f"  WARN: replay={replay2}, tid2={tid2} vs tid={tid}")
    except Exception as e:
        print(f"  FAIL: {e}")
        return

    # 3. Changed payload -> checksum conflict
    print("\n--- Phase 3: Changed Payload Rejection ---")
    modified_event = json.loads(body_str)
    modified_event["primary_contact"]["email"] = "different@test.truevow.local"
    m_payload_for_cs = {k: v for k, v in modified_event.items() if k != "checksum"}
    modified_event["checksum"] = hashlib.sha256(js_json_dumps(m_payload_for_cs).encode()).hexdigest()
    mod_body_str = js_json_dumps(modified_event)
    mod_body_bytes = mod_body_str.encode()
    headers3 = sign_request("POST", CANONICAL_PATH, mod_body_str, HMAC_SECRET, HMAC_KEY_ID)
    try:
        r3 = requests.post(f"{SAAS_ADMIN_URL}{CANONICAL_PATH}", headers=headers3,
                           data=mod_body_bytes, timeout=REQUEST_TIMEOUT)
        body3 = r3.json()
        ps3 = body3.get("processing_status", "N/A")
        print(f"  Changed payload: HTTP {r3.status_code}  status={ps3}")
        if ps3 == "REJECTED_CHECKSUM_CONFLICT":
            print("  PASS: Same handoff_id + different checksum -> REJECTED")
        else:
            print(f"  WARN: Expected REJECTED_CHECKSUM_CONFLICT, got {ps3}")
    except Exception as e:
        print(f"  FAIL: {e}")

    # 4. Concurrent same-name firm -> distinct slugs
    print("\n--- Phase 4: Concurrent Same-Name Firms ---")
    hid4a, event4a = make_handoff_payload(suffix="-a")
    hid4b, event4b = make_handoff_payload(suffix="-b")
    for label, hid_val, event_val in [("Firm A", hid4a, event4a), ("Firm B", hid4b, event4b)]:
        bs = js_json_dumps(event_val)
        hdrs = sign_request("POST", CANONICAL_PATH, bs, HMAC_SECRET, HMAC_KEY_ID)
        try:
            resp = requests.post(f"{SAAS_ADMIN_URL}{CANONICAL_PATH}", headers=hdrs,
                                data=bs.encode(), timeout=REQUEST_TIMEOUT)
            print(f"  {label}: HTTP {resp.status_code}  {resp.json().get('handoff_id', '?')}")
        except Exception as e:
            print(f"  {label}: FAIL ({e})")

    print("\nE2E run complete.")


def cmd_status():
    print(f"E2E EXECUTION ID: {EXECUTION_ID}")
    print(f"SYNTHETIC MARKER: {SYNTHETIC_MARKER}")
    print(f"SAAS ADMIN: {SAAS_ADMIN_URL}")
    print(f"CANONICAL PATH: {CANONICAL_PATH}")
    print()
    print("Manual verification queries for Supabase staging (jahhqcypxjkxwrfzpyxd):")
    print(f"  handoff_acknowledgments WHERE handoff_id LIKE '{EXECUTION_ID}%'")
    print(f"  tenant_accounts WHERE firm_name LIKE 'E2E Test Firm {EXECUTION_ID[:8]}%'")
    print(f"  tenant_onboarding_runs WHERE handoff_id LIKE '{EXECUTION_ID}%'")
    print(f"  platform_commands_outbox WHERE tenant_id IN (SELECT tenant_id FROM tenant_accounts WHERE firm_name LIKE 'E2E Test Firm {EXECUTION_ID[:8]}%')")


def cmd_cleanup():
    print(f"Cleanup for execution {EXECUTION_ID}")
    print()
    print("Run against Supabase staging (jahhqcypxjkxwrfzpyxd):")
    print(f"""
-- Cleanup synthetic E2E records
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT tenant_id FROM tenant_accounts
             WHERE firm_legal_name ILIKE 'E2E Test Firm {EXECUTION_ID[:8]}%'
    LOOP
        DELETE FROM system_audit_log WHERE tenant_id = r.tenant_id;
        DELETE FROM platform_commands_outbox WHERE tenant_id = r.tenant_id;
        DELETE FROM tenant_onboarding_steps WHERE tenant_id = r.tenant_id;
        DELETE FROM tenant_onboarding_runs WHERE tenant_id = r.tenant_id;
        DELETE FROM tenant_product_entitlements WHERE tenant_id = r.tenant_id;
        DELETE FROM mdm_events_outbox WHERE payload->>'tenant_id' = r.tenant_id::text;
        DELETE FROM handoff_acknowledgments WHERE tenant_id = r.tenant_id;
        DELETE FROM core_contacts WHERE tenant_id = r.tenant_id;
        DELETE FROM core_tenants WHERE tenant_id = r.tenant_id;
        DELETE FROM tenant_accounts WHERE tenant_id = r.tenant_id;
    END LOOP;
END $$;
""")


if __name__ == "__main__":
    cmds = {"validate": cmd_validate, "run": cmd_run, "status": cmd_status, "cleanup": cmd_cleanup}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(f"Usage: e2e_harness.py <{'|'.join(cmds)}>")
        sys.exit(1)
    cmds[sys.argv[1]]()
