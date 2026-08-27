# Full Commissioning Test Matrix — 62 Tests, 5 Gates

**Current status:** NOT COMMISSIONED
**Gate 0R:** Closed (contracts frozen, blockers resolved)
**Phases 3-4:** Conditional approval (implementation in progress)

---

## Gate 5A — Contract and Security (Must pass 100%)

| ID | Test | Critical | Status |
|---|---|---|---|
| 5A-01 | Valid HMAC-signed handoff reaches receiver | Yes | PASS |
| 5A-02 | Valid handoff payload creates contact + returns acknowledgment | Yes | PASS |
| 5A-03 | Minimum required payload fields enforced (no lead_id → 400) | Yes | PASS |
| 5A-04 | Idempotent replay returns original result (no duplicate rows) | Yes | PASS |
| 5A-05 | Missing HMAC signature headers rejected (401) | Yes | PASS |
| 5A-06 | Malformed signature rejected | Yes | — |
| 5A-07 | Incorrect signature rejected (wrong key) | Yes | — |
| 5A-08 | Correct signature over altered payload rejected | Yes | — |
| 5A-09 | Correct signature for wrong canonical path rejected | Yes | — |
| 5A-10 | Correct signature for wrong HTTP method rejected | Yes | — |
| 5A-11 | Unknown key ID rejected | Yes | — |
| 5A-12 | Expired timestamp (>5 min) rejected | Yes | — |
| 5A-13 | Future timestamp outside tolerance rejected | Yes | — |
| 5A-14 | Valid replay within replay window accepted (200 idempotent) | Yes | — |
| 5A-15 | Same handoff_id + different checksum → 409 Conflict + audit event | Yes | — |
| 5A-16 | Same application + different handoff_id accepted (new handoff) | Yes | — |
| 5A-17 | Legacy API key before 2026-09-01 accepted with warning | Yes | — |
| 5A-18 | Legacy API key on 2026-09-01 rejected (410 Gone) | Yes | — |
| 5A-19 | Invalid HMAC + valid legacy API key → still rejected (HMAC takes precedence) | Yes | — |
| 5A-20 | Fallback usage counter increments on legacy auth | No | — |
| 5A-21 | Fallback security audit event created | No | — |
| 5A-22 | Unsupported EventEnvelope version rejected | Yes | — |
| 5A-23 | Unsupported HandoffContract version rejected | Yes | — |
| 5A-24 | Missing authority_record_id rejected | Yes | — |
| 5A-25 | Invalid authority class rejected | Yes | — |
| 5A-26 | Missing policy_version rejected | Yes | — |
| 5A-27 | Unsupported sensitivity class rejected | No | — |
| 5A-28 | Checksum mismatch rejected | Yes | — |

---

## Gate 5B — State and Migration (Must pass 100%)

| ID | Test | Critical | Status |
|---|---|---|---|
| 5B-01 | All 44 legacy values mapped (0 unmapped) | Yes | — |
| 5B-02 | Total row count before == after migration | Yes | — |
| 5B-03 | No legacy value defaults to APPROVED_CUSTOMER | Yes | — |
| 5B-04 | No legacy value defaults to HANDOFF_PENDING | Yes | — |
| 5B-05 | No legacy value defaults to HANDED_OFF | Yes | — |
| 5B-06 | Unmapped records go to FAILED with metadata preserved | Yes | — |
| 5B-07 | CHECK constraint validates all post-migration rows | Yes | — |
| 5B-08 | Invalid transition rejected (DISCOVERED → APPROVED_CUSTOMER) | Yes | — |
| 5B-09 | All 26 transitions from registry enforceable | Yes | — |
| 5B-10 | Staging rollback: row counts restored | Yes | — |
| 5B-11 | Staging rollback: CHECK constraint re-added | Yes | — |
| 5B-12 | Staging rollback: application boots | No | — |
| 5B-13 | Staging rollback: no handoff duplication | Yes | — |
| 5B-14 | Staging rollback: no transition history corruption | No | — |
| 5B-15 | Duplicate migration execution idempotent | No | — |
| 5B-16 | Migration resumable after batch failure | No | — |
| 5B-17 | Pipeline stage column has no NULL values after migration | Yes | — |

---

## Gate 5C — MDM and Transactional Behavior (Must pass 100%)

| ID | Test | Critical | Status |
|---|---|---|---|
| 5C-01 | New organization created from handoff | Yes | — |
| 5C-02 | Existing organization without tenant resolved (no duplicate) | Yes | — |
| 5C-03 | Existing organization with tenant → new entitlements added (no duplicate tenant) | Yes | PASS |
| 5C-04 | Matching email + conflicting legal identity → manual review (no silent merge) | Yes | — |
| 5C-05 | Matching domain + conflicting organization → manual review | No | — |
| 5C-06 | Duplicate ContactPoint resolved (no duplicate insert) | Yes | — |
| 5C-07 | Tenant created with source_customer_candidate_id | Yes | — |
| 5C-08 | Product entitlements created per approved_products | Yes | — |
| 5C-09 | Onboarding case created | Yes | — |
| 5C-10 | CSM assigned | No | — |
| 5C-11 | Transaction rollback: org created but entitlements fail → all rolled back | Yes | — |
| 5C-12 | Transaction rollback: tenant created but audit fails → all rolled back | Yes | — |
| 5C-13 | Unapproved product in entitlements rejected | Yes | — |
| 5C-14 | Idempotent replay: same organization_id returned | Yes | — |
| 5C-15 | Idempotent replay: same tenant_id returned | Yes | — |
| 5C-15a | Idempotent replay: same entitlement IDs returned | Yes | — |
| 5C-15b | Idempotent replay: same onboarding reference returned | No | — |
| 5C-15c | Idempotent replay: no additional database rows created | Yes | — |
| 5C-15d | Idempotent replay: no duplicate outbox event emitted | Yes | — |
| 5C-15e | Idempotent replay: no duplicate audit mutation | Yes | — |
| 5C-15f | Idempotent replay: response includes `idempotent_replay: true` | No | — |
| 5C-15g | First processing: 201 Created; Idempotent replay: 200 OK with original result | No | — |
| 5C-16 | Tenant created with account_status: 'onboarding' (not 'active') | Yes | — |

---

## Gate 5D — End-to-End Resilience

| ID | Test | Critical | Status |
|---|---|---|---|
| 5D-01 | Full trace: discovery → enrichment → ... → acknowledgment | Yes | — |
| 5D-02 | SaaS Admin unavailable → outbox retry → eventual delivery | Yes | — |
| 5D-03 | Delivery worker interruption → resume → no duplicate delivery | Yes | — |
| 5D-04 | Network response loss after SaaS Admin commits → retry returns original (no duplicate) | Yes | — |
| 5D-05 | Duplicate delivery → idempotent (original result returned) | Yes | — |
| 5D-06 | Invalid signature → dead-letter after max retries | Yes | — |
| 5D-07 | Identity conflict → manual review queue (not silently resolved) | No | — |
| 5D-08 | Outbox retry with exponential backoff | No | — |
| 5D-09 | Dead-letter path: unrecoverable → alert + manual intervention | No | — |
| 5D-10 | Correlation ID survives all cross-service boundaries | Yes | — |
| 5D-11 | Causation chain unbroken (each event references causing event) | Yes | — |

---

## Gate 5E — Trace Reconstruction

| ID | Test | Critical | Status |
|---|---|---|---|
| 5E-01 | Given customer_candidate_id → reconstruct source lead | Yes | — |
| 5E-02 | Given customer_candidate_id → reconstruct application | Yes | — |
| 5E-03 | Given customer_candidate_id → reconstruct qualification | Yes | — |
| 5E-04 | Given customer_candidate_id → reconstruct approval authority | Yes | — |
| 5E-05 | Given customer_candidate_id → reconstruct HandoffPackage | Yes | — |
| 5E-06 | Given customer_candidate_id → reconstruct EventEnvelope | Yes | — |
| 5E-07 | Given customer_candidate_id → reconstruct delivery attempts | No | — |
| 5E-08 | Given customer_candidate_id → reconstruct SaaS Admin receipt | Yes | — |
| 5E-09 | Given customer_candidate_id → reconstruct Organization + ContactPoints + Tenant + entitlements | Yes | — |
| 5E-10 | Given customer_candidate_id → reconstruct onboarding + acknowledgment | Yes | — |
| 5E-11 | No missing correlation links between any pair of adjacent events | Yes | — |
| 5E-12 | No missing causation links between any pair of adjacent events | Yes | — |

---

## By Severity

| Gate | Total | Critical | Currently Passing |
|---|---|---|---|
| 5A — Contract and Security | 28 | 22 | 5 (5A-01 through 5A-05) |
| 5B — State and Migration | 17 | 12 | 0 |
| 5C — MDM and Transactional | 23 | 16 | 1 (5C-03) |
| 5D — Resilience | 11 | 7 | 0 |
| 5E — Trace Reconstruction | 12 | 8 | 0 |
| **Total** | **62** | **65** | **6** |

---

## Gate Closure Criteria

| Gate | Requirement |
|---|---|
| 5A | 28/28 pass (100%) — includes all 22 critical + 6 non-critical |
| 5B | 17/17 pass (100%) — no data integrity compromise allowed |
| 5C | 23/23 pass (100%) — no partial state or silent merge allowed |
| 5D | 11/11 pass (100%) — requires retry, idempotency, and distributed recovery |
| 5E | 12/12 pass (100%) — requires unbroken correlation chain |

No percentage threshold. All gates must reach 100% for COMMISSIONED status.
