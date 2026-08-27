---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/api-and-interface-design/SKILL.md
imported: 2026-08-12T17:53:11.232824+00:00
skill_name: api-and-interface-design
---

---
name: api-and-interface-design
description: TrueVow contract-first API design. HMAC service-to-service auth, idempotency, correlation IDs. Use /to-spec for the spec, then this for the contracts.
---

# /api-and-interface-design

TrueVow contract-first API patterns. Use `/to-spec` (Pocock) for the spec document, then apply these platform-specific contract rules.

## Service-to-Service Contract

```text
key_id + timestamp + HTTP method + canonical path + SHA-256(body) + HMAC
```
- Clock-skew guard: 300s replay window
- Per-service key isolation (e.g., `tv-sales-ops-to-saas-admin-v1`)
- Never reuse another service's key/secret

## Required Fields

Every canonical event/command:
```
command_id / event_id
schema_version
tenant_id / customer_id
correlation_id + causation_id
idempotency_key
timestamp
sender identity
```

## Idempotency Rules

- Same event_id + same payload → accepted (idempotent), one effect
- Same event_id + different payload → 409 CONFLICT
- Concurrent duplicates → one authoritative effect
- Persist receipt evidence: `payload_checksum`, `received_at`, `completed_at`

## Correlation Chain

Throughout the Golden Journey:
```
lead_id → application_id → handoff_package_id → customer_id → tenant_id → onboarding_run_id → subscription_id
```

## Anti-Patterns

- Generic `X-API-Key` for canonical contracts → use HMAC instead
- `DELIVERY_MODE=disabled` returning `SUCCEEDED` → never fabricate delivery evidence
- Command queued ≠ fact occurred → transport suppressed ≠ delivered

## Related
- `/to-spec` — generate the spec document
- TrueVow canonical-decisions.md — binding platform-wide rules
