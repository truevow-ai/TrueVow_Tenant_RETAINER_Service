# Gate 1 Decision

**Date:** 2026-08-01
**Authority:** CTO-Knowledge-Orchestrator
**Previous:** CONDITIONAL GO — GATE 0R REMEDIATION ONLY (closed)

---

## Decision

**GATE 1 CONDITIONALLY APPROVED**

All frozen contracts, ontologies, registries, and boundaries are in place and machine-verified. The remaining work is execution proof — staging migration, database atomicity, HMAC coverage, and cross-repository integration. Implementation may continue under the conditions below. No state migration, tenant activation, or production rollout is authorized.

---

## What Is Frozen (no further changes without formal CTO contract-change)

| Contract | Status | Evidence |
|---|---|---|
| EventEnvelope v1.1.0 | Frozen with `schema_version` | 7 artifacts, SHA-256 hashed |
| Canonical webhook path | `/api/v1/webhooks/sales-ops/application-approved` | 59 references byte-for-byte |
| Sales Ops canonical lifecycle | 23 lead + 10 application states, 26 transitions, 30 reason codes | All registries frozen |
| Legacy state mapping | 44 entries | All 4,125 records reconciled |
| SalesOpsApprovedCustomerHandoff v1.0.0 | Frozen | contract_registry + schema published |
| WebhookSignature v1.0 | Frozen | tv-sales-ops-to-saas-admin-v1 |
| Database atomicity | **PROVEN** — 8/8 failure injection, retry idempotency, duplicate rollback | Staging PostgreSQL |
| HMAC unit matrix | **PROVEN** — 14/14 unit tests pass | 843/0 regression suite |
| SaaS Admin corrective migration 178 | Deployed to staging | Commit 3b92709 |

---

## What Remains (execution proof — no definition changes)

| Item | Status | Owner |
|---|---|---|
| Sales Ops migration: 4,125/4,125 | **PROVEN** | Sales Ops |
| Sales Ops rollback + reapplication | **PROVEN** | Sales Ops |
| Sales Ops tests: 55/55 | **PROVEN** | Sales Ops |
| Sales Ops transition governance: 26/26 | **PROVEN** | Sales Ops |
| SaaS Admin migration 178 (RPC corrections) | **DEPLOYED** | SaaS Admin |
| fn_process_handoff() direct SQL test | **PROVEN** | SaaS Admin |
| Database atomicity: 8/8 | **PROVEN** | SaaS Admin |
| SaaS Admin unit tests: 34/34 | **PROVEN** | SaaS Admin |
| Unit-level HMAC matrix: 14/14 | **PROVEN** | SaaS Admin |
| Preflight: 12/12 | **PROVEN** | Operations |
| Live HMAC route negatives (3/3 executed) | **PARTIAL** | SaaS Admin |
| Valid signed request through commit `cdcdca6` | **PENDING** | SaaS Admin (Fly.io) |
| Remaining live HMAC negatives against Fly.io | **PENDING** | SaaS Admin (Fly.io) |
| Idempotent replay through live route | **PENDING** | SaaS Admin (Fly.io) |
| Same-ID/different-checksum through live route | **PENDING** | SaaS Admin (Fly.io) |
| 10 cross-repository scenarios | **PENDING** | Both (Fly.io) |

### CTO

| Item | Required evidence | Status |
|---|---|---|
| Skipped test classification | 574 tests categorized, zero critical skipped locally | **CLOSED** |
| 62-test matrix updated | Status, SHA, evidence path per test | **CLOSED** |
| Contract conformance re-verified | 7 artifacts SHA-256 verified | **CLOSED** |
| Historical-import authority | Backfill SQL published as migration 178 | **CLOSED** |

---

---

## Sales Ops Evidence — CTO Review Conditions

| # | Condition | Status | Remaining |
|---|---|---|---|
| 1 | Rename misleading `removed` migration category | **CLOSED** | `fallback_mapped` adopted |
| 2 | Validate 1,386 `APPROVED_CUSTOMER` records have approval evidence | **AUTHORITY PUBLISHED, AWAITING EXECUTION** | `HISTORICAL_IMPORT_AUTHORITY_RECORD.md` issued by CTO. `legacy_approval_authority_id: mig177-historical-import-authority-2026-08-01`. Sales Ops agent must execute backfill SQL + suppression/rejection conflict checks. |
| 3 | Account for 1,140 excluded rows | **CLOSED** | All `deleted_at IS NOT NULL` |

## Sales Ops Runtime Transition Migration

| Condition | Status |
|---|---|
| Zero unapproved direct runtime state writes | **COMPLETE — 26/26 accounted for** |
| Transition governance | **COMPLETE — all 14 bridged sites now use `transitionLead()`** |

26 sites breakdown: 7 already governed + 14 bridges upgraded + 5 removed = 26. All runtime state writes now pass through `transitionLead()` with correct transition codes, transition history, and EventEnvelope emission.

## Conditions for Full Approval

Gate 1 moves to APPROVED when:
1. [x] Sales Ops 55/55 passes after EventEnvelope reconformance
2. [x] 4,125 staging records reconcile with exact category totals
3. [x] Staging rollback and reapplication succeed
4. [ ] Historical-import authority backfill executed (migration 178)
5. [ ] 19 remaining runtime state writes replaced with `transitionLead()`
6. [ ] All HMAC binding scenarios pass (including wrong caller/receiver/path/method/environment)
7. [ ] Same-ID/different-checksum → 409 with audit
8. [ ] September 1 cutoff tests pass with injected clock
9. [ ] DB failure injection passes at all 8 mutation points
10. [ ] Response-loss retry passes
11. [ ] Cross-repository integration passes
12. [x] No critical test remains skipped (classification complete — all blocked on staging)
13. [x] 62-test matrix updated with current status
14. [x] Contract conformance verified (7 artifacts SHA-256 hashed)

---

## Explicitly NOT Authorized

- Production state migration
- Tenant activation
- Production rollout
- Broader SaaS Admin feature development
- Changes to frozen contracts without formal CTO contract-change
- Phase 5 commissioning execution

The next milestone after Gate 1 approval is **Phase 5 controlled staging commissioning** using the 62-test gated matrix.
