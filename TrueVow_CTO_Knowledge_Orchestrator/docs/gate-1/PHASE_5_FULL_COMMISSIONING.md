# Phase 5 — Full Commissioning (Gated)

**Phase:** 5 of 5
**Authority:** CTO-Knowledge-Orchestrator
**Prerequisite:** Phase 3 APPROVED and Phase 4 CERTIFIED
**Current status:** NOT COMMISSIONED (6 of 62 tests passing)

---

## Decision

**NOT COMMISSIONED.**

The 6 passing tests (5A-01 through 5A-05, 5C-03, plus the two smoke tests) establish the receiver path exists. They do not yet prove the security contract, transactional integrity, migration safety, or end-to-end resilience. Commissioning requires 62/62 tests passing across all 5 gates.

---

## Gate Structure

Do not run all 62 tests as one undifferentiated batch. Use 5 sequential gates. Each gate must reach 100% pass before the next begins.

### Gate 5A — Contract and Security (28 tests)

**Status:** 5/28 passing (18%)

What this gate proves: the webhook is safe against forgery, replay, path manipulation, and contract violations. The HMAC signing contract is enforced at both sender and receiver. The legacy API key path closes on September 1, 2026.

### Gate 5B — State and Migration (17 tests)

**Status:** 0/17 passing (0%)

What this gate proves: the 44-entry legacy mapping is exhaustive. No record silently defaults to a successful lifecycle state. The CHECK constraint validates all rows. Rollback is proven in staging. The migration is resumable and idempotent.

### Gate 5C — MDM and Transactional Behavior (23 tests)

**Status:** 1/23 passing (4%)

What this gate proves: organization and contact resolution is deterministic and deduplicates correctly (no silent merge). Tenant creation is a single atomic transaction — partial failure rolls back completely. Idempotent replay returns the same result with all assertions verified (not just HTTP status). Same-ID/different-checksum produces 409 Conflict with audit event.

### Gate 5D — End-to-End Resilience (11 tests)

**Status:** 0/11 passing (0%)

What this gate proves: the system survives SaaS Admin unavailability, worker interruption, network response loss after commit, duplicate delivery, and invalid signatures. The classic distributed-systems failure (commit succeeds, response lost, retry) returns the original result without duplication.

### Gate 5E — Trace Reconstruction (12 tests)

**Status:** 0/12 passing (0%)

What this gate proves: given one `customer_candidate_id`, every artifact in the complete trace can be reconstructed with unbroken correlation and causation chains. No missing links between adjacent events.

---

## Previously Defined 25 Scenarios → Gate Mapping

| Scenario | Gates covered |
|---|---|
| S1 Happy path | 5A, 5C, 5D, 5E |
| S2 Existing org no tenant | 5C |
| S3 Existing tenant | 5C |
| S4 Ambiguous org | 5C |
| S5 Duplicate handoff | 5A, 5C |
| S6 Altered duplicate | 5A, 5C |
| S7 SaaS Admin unavailable | 5D |
| S8 Delivery retry | 5D |
| S9 Worker interruption | 5D |
| S10 Invalid signature | 5A |
| S11 Expired signature | 5A |
| S12 Replay attempt | 5A, 5D |
| S13 Legacy key before cutoff | 5A |
| S14 Legacy key after cutoff | 5A |
| S15 Unsupported version | 5A |
| S16 Invalid transition | 5B |
| S17 Approval without authority | 5B |
| S18 Cohort phases inaccessible | 5B |
| S19 App2→App3 blocked | 5B |
| S20 Entitlement mismatch | 5C |
| S21 Transaction rollback | 5C |
| S22 Audit reconstruction | 5E |
| S23 Correlation chain | 5E |
| S24 Portal no secrets | 5A |
| S25 No activation during handoff | 5C |

---

## Commissioning Decision Criteria

### COMMISSIONED FOR CONTROLLED PRODUCTION

All 5 gates must reach 100%:
- 5A: 28/28
- 5B: 17/17
- 5C: 23/23
- 5D: 11/11
- 5E: 12/12

Plus:
- Verified rollback (migration + transaction)
- Verified observability (audit events, metrics, alerts)
- Confirmed 2026-09-01 legacy-auth cutoff
- All 15 evidence artifacts delivered

### CONDITIONALLY COMMISSIONED

A subset of gates may pass while defects remain in non-critical tests only (those marked non-critical in the matrix). Conditional commissioning specifies which scenarios are approved and which are blocked.

### NOT COMMISSIONED

Any failure in a critical test, any security boundary failure, any data integrity failure, or any unverified rollback = NOT COMMISSIONED. The current status.

---

## Next CTO Report Must Include

1. Canonical endpoint-path decision
2. Phase 3 staging dry-run totals
3. Rollback execution evidence
4. Phase 4 HMAC test results (all 28 Gate 5A tests)
5. Identity-resolution test results (5C-01 through 5C-06)
6. Transaction-failure test results (5C-11, 5C-12)
7. Idempotency and concurrent-replay results (5C-14 through 5C-15g)
8. Legacy API-key cutoff test (5A-18 with post-2026-09-01 clock)
9. 62-test matrix status by gate
10. Remaining defects by severity

---

## 1. Complete Trace

The commissioning execution must reconstruct every step from lead discovery to tenant activation acknowledgment:

```text
Phase A: Sales Ops Lead Pipeline
  Lead discovery (scraper or website intake)
  → Normalization (identity, firm name, website)
  → Profiling (firmographics: practice areas, size, bar memberships)
  → Contact enrichment (emails pattern-guessed, phones E.164 normalized)
  → Validation pending (SMTP verify, phone classification)
  → Verified (email_verified=true or phone_type populated)
  → Scored (lead_score computed from enrichment quality)
  → QA pending (score >= threshold → human review queue)
  → Outreach approved (QA passed or auto-approved)
  → Campaign eligible (suppression check, jurisdiction match, practice area match)
  → In campaign (outreach sequence active)
  → Engaged (positive response: reply, click, demo request)

Phase B: Sales Ops Application Pipeline
  → Application started (lead creates CustomerApplication)
  → Application submitted (form completed, firm identity validated)
  → Qualification review (human reviewer evaluates commercial fit)
  → Approved customer (commercial approval, HUMAN_ONLY authority)

Phase C: Sales Ops Handoff
  → Handoff package sealed (immutable, checksummed, versioned)
  → Handoff pending (awaiting SaaS Admin delivery)
  → EventEnvelope v1.1.0 emitted (18 fields, tenant_id=null, authority_domain=salesops)

Phase D: Cross-Service Webhook
  → HMAC-SHA256 signed request (X-TrueVow-Key-Id, X-TrueVow-Timestamp, X-TrueVow-Signature)
  → POST /api/v1/webhooks/sales-ops/application-approved
  → SaaS Admin verifies signature, timestamp, replay protection

Phase E: SaaS Admin Processing
  → Handoff validation (schema check, checksum verification)
  → Idempotency check (handoff_id already processed?)
  → Organization resolution (dedup by legal_name + jurisdiction → ENT-012)
  → ContactPoint resolution (dedup by email + phone → ENT-014)
  → Tenant creation (ENT-001 with source_customer_candidate_id)
  → Product entitlement configuration (one row per approved product)
  → Onboarding case creation
  → CSM assignment
  → Provisioning request record

Phase F: Acknowledgment and Downstream
  → tenant.created event emitted (EventEnvelope v1.1.0, tenant_id=uuid)
  → HMAC-SHA256 acknowledgment to Sales Ops (POST /api/v1/webhooks/sales-ops/handoff-acknowledged)
  → Sales Ops updates lead to HANDED_OFF with tenant_id
  → INTAKE receives tenant.created webhook
  → CSM receives onboarding notification
```

---

## 2. Commissioning Scenarios (25 Mandatory)

Each scenario must produce pass/fail evidence with trace reconstruction.

### S1: New Approved Customer (Happy Path)

Full trace from lead discovery to tenant activation acknowledgment. All 6 phases execute without error.

### S2: Existing Organization Without Tenant

Organization exists in SaaS Admin (prior contact, prior demo, prior inquiry) but no tenant. Handoff resolves to existing ENT-012, creates new ENT-001 + entitlements.

### S3: Existing Tenant

Organization already has a tenant (different product, prior trial). Handoff resolves to existing ENT-012 and ENT-001. Adds new product entitlements without duplicate tenant.

### S4: Ambiguous Organization Identity

Two organizations match the handoff firm data (same jurisdiction, similar name). SaaS Admin flags for manual resolution. Handoff enters pending-manual-review state. Not silently auto-matched.

### S5: Duplicate Handoff

Same handoff_id processed twice. Second attempt returns 200 with original tenant_id. No duplicate tenant, no duplicate entitlements, no duplicate contacts.

### S6: Altered Duplicate Handoff

Same handoff_id but different checksum (payload tampered after initial delivery). Second attempt rejected with 409 conflict. Original result preserved.

### S7: SaaS Admin Unavailable

Sales Ops outbox delivery worker retries with exponential backoff. Handoff remains in HANDOFF_PENDING or RETRY_SCHEDULED. Sales Ops continues operating — no synchronous SaaS Admin dependency.

### S8: Delivery Retry

After transient failure, delivery worker retries. Same handoff_id, same checksum. SaaS Admin returns idempotent result. Sales Ops receives acknowledgment.

### S9: Worker Interruption

Delivery worker crashes mid-delivery. On restart, outbox picks up the interrupted message. Duplicate delivery is idempotent on SaaS Admin side.

### S10: Invalid Signature

HMAC headers present but signature doesn't match body. SaaS Admin returns 401. Outbox marks as dead-lettered after max retries.

### S11: Expired Signature

HMAC timestamp older than 5 minutes. SaaS Admin returns 401. Delivery worker regenerates signature with fresh timestamp and retries.

### S12: Replay Attempt

Valid signature from a prior delivery replayed. SaaS Admin detects replay via idempotency store. Returns 200 with original result (not re-processed).

### S13: Legacy API Key Before Cutoff

X-API-Key header present, HMAC headers absent, current date < 2026-09-01. SaaS Admin accepts with warning log. Fallback counter incremented.

### S14: Legacy API Key After Cutoff

Same as S13 but current date >= 2026-09-01. SaaS Admin rejects with 410 Gone. Legacy fallback path is dead.

### S15: Unsupported Contract Version

Handoff payload has `handoff_version: 2` (future). SaaS Admin rejects with 400 — schema validation fails for unknown version.

### S16: Invalid State Transition

Attempt to transition lead directly from DISCOVERED to APPROVED_CUSTOMER (skip 12 intermediate states). Transition rejected by PipelineStateManager or DB trigger.

### S17: Application Approval Without Authority

Automated agent attempts application approval with `authority_class: salesops_act_bounded`. Rejected — approval requires HUMAN_ONLY authority.

### S18: Removed Cohort Phases Remain Inaccessible

Attempt to execute Phase 7 or Phase 8 of the pipeline. Pipeline runner refuses. Cohort scripts are not importable by default pipeline.

### S19: Direct App2-to-App3 Call Blocked

Attempt to call `provisionTenant()` from Sales Ops code. Method throws unconditionally. Architecture test confirms no App2→App3 call paths exist.

### S20: Entitlement Mismatch Blocked

Handoff specifies `approved_products: ["INTAKE"]` but tenant provisioning attempts to add SETTLE entitlements. Rejected — entitlements must match approved products.

### S21: Transaction Rollback

Tenant creation succeeds but entitlement configuration fails mid-transaction. Entire SaaS Admin transaction rolls back. No partial state committed. Handoff remains retryable.

### S22: Complete Audit Reconstruction

Every operation in the trace produces an audit event with correlation_id, causation_id, actor, authority, policy version. Full trace reconstructable from audit events alone.

### S23: Full Correlation and Causation Chain

correlation_id from Sales Ops discovery event survives through all subsequent events. causation_id chain is unbroken: each event references the event that directly caused it.

### S24: Customer Portal Has No Webhook Secret

Environment variable scan confirms no webhook secrets, signing keys, or API keys in Customer Portal config. Portal is a read-only consumer of Shared Platform state.

### S25: No Tenant Activation During Handoff Processing

Tenant is created with `account_status: 'onboarding'` (not `active`). Activation is a separate, deliberate command requiring commissioning gate approval. Handoff processing does not activate tenants.

---

## 3. Reconciliation with Original 43 Commissioning Tests

The 25 scenarios above must be cross-referenced with the original 43 tests from `SALES_OPS_COMMISSIONING_TEST_MATRIX.md`. This is additive — the 25 scenarios supplement, not replace, the original matrix.

### Coverage Map

| Original Test Group | Tests | Covered by Scenario(s) |
|---|---|---|
| O-01 to O-06 (Ontology) | 6 | S1, S16, S17 (state names, transitions, authority) |
| S-01 to S-06 (State transitions) | 6 | S1, S16 (full lifecycle, invalid transition) |
| A-01 to A-05 (Authority) | 5 | S17 (automated agent blocked), S19 (App2→App3 blocked) |
| P-01 to P-05 (Pipeline) | 5 | S1 (cross-source alignment), S18 (cohort removed) |
| B-01 to B-10 (Bridge) | 10 | S2, S3, S4, S5, S6, S7, S8, S9, S20, S21, S22, S25 |
| C-01 to C-04 (Contract) | 4 | S10, S11, S12, S15 |
| F-01 to F-07 (Failure) | 7 | S7, S8, S9, S10, S11, S12, S21 |

### Combined Test Count

| Domain | Original | Scenario | Combined unique |
|---|---|---|---|
| Ontology | 6 | +0 | 6 |
| State transitions | 6 | +1 (S16 adds new) | 7 |
| Authority | 5 | +2 (S17, S19 new) | 7 |
| Pipeline | 5 | +1 (S18 new) | 6 |
| Bridge (handoff) | 10 | +8 (S2-S6, S8-S9, S21, S25 new) | 18 |
| Contract (webhook) | 4 | +4 (S10-S12, S15 new) | 8 |
| Failure | 7 | +3 (S7, S9, S21 new) | 10 |
| **Total** | **43** | **+19** | **62** |

---

## 4. Evidence Package Checklist

| # | Artifact | Required |
|---|---|---|
| 1 | Final test matrix (combined 62 tests) | Yes |
| 2 | Test execution results (pass/fail/skip per test) | Yes |
| 3 | Cross-service trace samples (correlation_id chain for S1) | Yes |
| 4 | Database reconciliation (row counts before/after migration + handoff) | Yes |
| 5 | Security test results (HMAC negative scenarios N1-N12) | Yes |
| 6 | Failure injection results (S7, S8, S9, S21) | Yes |
| 7 | Performance measurements (handoff latency, tenant creation latency) | Yes |
| 8 | Residual risk register (any untested path, known limitation) | Yes |
| 9 | Rollback evidence (migration rollback test, transaction rollback test) | Yes |
| 10 | Contract version inventory (all frozen contracts with versions) | Yes |
| 11 | Production configuration checklist (env vars, keys, feature flags) | Yes |
| 12 | S1 full trace reconstruction (from discovery to acknowledgment) | Yes |
| 13 | S24 Customer Portal security scan results | Yes |
| 14 | S13/S14 legacy auth cutoff verification | Yes |
| 15 | `tenant_id` null handling in all consumers | Yes |

---

## 5. Commissioning Decision Criteria

### COMMISSIONED FOR CONTROLLED PRODUCTION

Requires:
- 100% critical contract tests pass
- 100% trust-boundary tests pass
- 100% HMAC and replay tests pass
- 100% implemented state-transition tests pass
- No unresolved critical or high defect
- Verified rollback (migration + transaction)
- Verified observability (audit events, metrics, alerts)
- Verified end-to-end trace (S1 correlation chain unbroken)
- Confirmed 2026-09-01 legacy-auth cutoff
- All 15 evidence artifacts delivered

### CONDITIONALLY COMMISSIONED

A subset may pass while defects remain in non-critical areas. Conditional commissioning specifies which scenarios are approved for production and which are blocked.

### NOT COMMISSIONED

Any critical or high defect, any security boundary failure, any data integrity failure, or any unverified rollback = NOT COMMISSIONED.

---

## Current Status

**NOT YET COMMISSIONED.** Awaiting completion of:
- Phase 3 state migration dry-run
- Phase 4 SaaS Admin handoff consumer implementation
- Phase 4 HMAC cutoff enforcement
- Phase 4 event builder equivalence verification
- 62 commissioning tests execution

The target is controlled production under the conditions defined in this document.
