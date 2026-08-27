# TrueVow Cross-Service Controlled Pilot — Final Recommendation

**From:** CTO Orchestrator & Release Architecture Reviewer (Yasha)
**Date:** 2026-07-31
**Recommendation:** NOT APPROVED

---

## Frozen Release Candidate v2

| # | Service | Branch | Commit SHA | State |
|---|---------|--------|------------|-------|
| 1 | INTAKE (Tenant Application) | main | `5e44f93` | CLEAN |
| 2 | RETAINER | master | `28a9ea4` | CLEAN (service code; monorepo docs dirty) |
| 3 | SaaS Admin (Shared Platform) | main | `88d4c2e` | DIRTY (4 untracked helper files) |
| 4 | TRACE | main | `3eb936c` | CLEAN |
| 5 | Customer Portal | master | `29d3edc` | CLEAN |
| 6 | Client Portal | — | — | NOT RECORDED |

### Migration Revisions
| SaaS Admin | RETAINER | TRACE | INTAKE |
|------------|----------|-------|--------|
| 174 | 0008 | 0017 | — |

---

## QA Evidence Summary

### Static Analysis & Unit Tests (Tasks executed by independent QA agent)

| Task | Status | Details |
|------|--------|---------|
| RETAINER webhook tests | **PASS** | 15/15 |
| SaaS Admin webhook tests | **FAIL** | 16/18 (D1, D2) |
| TRACE golden fixture tests | **NOT_EXECUTED** | Missing `reportlab` dependency |
| INTAKE webhook tests | **NOT_EXECUTED** | Test file missing (D4) |
| Customer Portal tests | **NOT_EXECUTED** | No test files found |

### Live Cross-Service Testing (Phases 6-20)

| Phase | Status |
|-------|--------|
| Primary lifecycle | **NOT_EXECUTED** — 0/5 services reachable |
| Webhook security (48 scenarios) | **NOT_EXECUTED** |
| Idempotency chain | **NOT_EXECUTED** |
| Contract schema validation | **NOT_EXECUTED** |
| Tenant isolation | **NOT_EXECUTED** |
| Authority tests | **NOT_EXECUTED** |
| Portal scope | **NOT_EXECUTED** |
| Client Portal browser | **NOT_EXECUTED** |
| Customer Portal browser | **NOT_EXECUTED** |
| Failure paths | **NOT_EXECUTED** |
| Retry/delivery | **NOT_EXECUTED** |
| Raw-body edge cases | **NOT_EXECUTED** |
| Key rotation | **NOT_EXECUTED** |
| Legacy cutoff | **NOT_EXECUTED** |
| RLS role validation | **NOT_EXECUTED** |
| Migration safety | **NOT_EXECUTED** |
| Observability | **NOT_EXECUTED** |

---

## Defects — Severity Assessment

### Severity 2 (Blocks pilot approval)

| ID | Service | Owner | Description |
|----|---------|-------|-------------|
| **D1** | SaaS Admin | ghous-isb | Trailing-slash canonicalization in `webhook-auth.ts:293` — `path.replace(/\/+$/, '')` makes `/activate/` match signed `/activate`, defeating wrong-path rejection. Python RETAINER implementation correctly uses raw path. |
| **D3** | RETAINER | ghaus-fsd | Per-service key isolation not enforced in default code path — `_resolve_secret` at `webhook_signature.py:122-124` maps ALL per-service registry keys to same fallback secret (`intake_webhook_secret`). Production with plain-string secret has INTAKE→RETAINER and RETAINER→SaaS Admin sharing credentials. |
| **D4** | INTAKE | ghaus-fsd | Webhook signature contract test file missing — `tests/test_webhook_signature_contract.py` does not exist. Cannot validate INTAKE signing against frozen WebhookSignature v1.0 contract. |

### Severity 3 (Does not block, should fix)

| ID | Service | Owner | Description |
|----|---------|-------|-------------|
| **D2** | SaaS Admin | ghous-isb | Secondary key test infrastructure failure — cached key registry ignores `TRUEVOW_WEBHOOK_SECONDARY_KEYS` set mid-test. Test infra only, not production. |
| **D5** | TRACE | yasha | Golden fixture tests blocked by missing `reportlab` dependency in local Python environment. Environment issue, not code. |

---

## Architecture Review

### Canonical Ownership Verification

| Invariant | Status | Evidence |
|-----------|--------|----------|
| INTAKE owns intake and candidate submission | **CONFIRMED** | Outbox sends `candidate.submitted_for_representation_review` |
| RETAINER owns engagement and activation preparation | **CONFIRMED** | `activation.py:157-159` — checklists and activation command |
| SaaS Admin is canonical Matter activation authority | **CONFIRMED** | `migration 170` — `matter_activations` table with anti-dual-activation trigger |
| TRACE consumes `matter.activated` idempotently | **CONFIRMED** | `business_events.event_id` PRIMARY KEY |
| Shared Platform owns portal identity and grants | **CONFIRMED** | `migration 174` — `client_portal_access_grants` + `fn_upgrade_portal_access_on_activation` |
| Shared Platform adds MATTER_* permissions | **CONFIRMED** | Trigger inserts 5 MATTER_* scopes at line 272 |
| RETAINER never grants MATTER_* scopes | **CONFIRMED** | `portal.py` grants only ENGAGEMENT_* scopes. `activation.py` transitions to ENGAGEMENT_HISTORY. Tests assert MATTER_* NOT in scopes. |
| RETAINER transitions only to ENGAGEMENT_HISTORY | **CONFIRMED** | `activation.py:157-159` |
| Webhook keys restricted by caller/receiver/path/method | **PARTIAL** | SaaS Admin and TRACE properly isolated. RETAINER default code path shares secrets across relationships (D3). INTAKE uses single key config. |
| Event/command idempotency enforced | **CONFIRMED** | DB constraints exist at all 3 hops |
| No direct cross-product DB writes | **CONFIRMED** | All inter-service state changes via signed webhooks |
| Tenant boundaries are fail-closed | **NOT TESTED LIVE** | Static analysis shows RLS policies exist; live tenant isolation tests not executed |

### Security Boundary Assessment

| Boundary | Status |
|----------|--------|
| Authentication = WebhookSignature v1.0 HMAC-SHA256 | **PASS** — RETAINER 15/15 |
| Per-relationship key isolation | **DEFECT D3** — RETAINER shares secrets in default path |
| Raw body hashing (no JSON reserialization) | **PASS** — `raw_body_hash_matches` test passes |
| 5-minute replay window | **PASS** — confirmed by EXPIRED/FUTURE timestamp tests |
| Timing-safe comparison | **PASS** — `hmac.compare_digest` used at line 107 |
| Signed route query-string prohibition | **NOT IMPLEMENTED** — no QS rejection in RETAINER/SaaS Admin code |
| Trailing-slash path canonicalization | **DEFECT D1** — SaaS Admin strips trailing slashes on verify |
| Legacy auth cutoff | **NOT TESTED LIVE** |

---

## Environment Status

| Item | Status |
|------|--------|
| INTAKE (3022) | UNREACHABLE |
| RETAINER (3038) | UNREACHABLE |
| SaaS Admin (3001) | UNREACHABLE |
| TRACE (3036) | UNREACHABLE |
| Customer Portal (3031) | UNREACHABLE |
| Client Portal | NOT REGISTERED |
| Staging Supabase | NOT CONFIRMED |
| Docker | NOT_DEPLOYED |
| SigNoz | UNKNOWN |

**Gate condition FAILED:** Test plan Section P0 requires all services healthy before QA execution.

---

## Rationale for NOT APPROVED

The test plan defines: **"No Severity 1 or Severity 2 defect may remain open for controlled-pilot approval."**

Three Severity-2 defects remain unresolved:
1. **D1 (SaaS Admin):** Trailing-slash canonicalization defeats wrong-path rejection
2. **D3 (RETAINER):** Per-service key isolation not enforced in default code path — cross-relationship secret reuse
3. **D4 (INTAKE):** Missing webhook signature contract tests

Additionally:
- No staging services are deployed or reachable.
- 0 of 5 services respond to health checks.
- All live cross-service testing (Phases 6-20) is NOT_EXECUTED.
- Client Portal is not registered in the release snapshot.
- SaaS Admin working tree remains dirty (4 untracked files).
- TRACE golden fixture tests blocked by environment dependency.

**The primary lifecycle (Phase 1) has never been executed end-to-end against staging.**

---

## Requirements for Re-Evaluation

To transition from NOT APPROVED to CONDITIONALLY APPROVED or APPROVED:

### Must-fix (Severity 2)
- [ ] **D1:** ghaus-fsd (or ghous-isb) — Fix SaaS Admin `webhook-auth.ts:293` to NOT strip trailing slashes on verify
- [ ] **D3:** ghaus-fsd — Fix RETAINER `webhook_signature.py:122-124` to resolve per-service keys independently in the primary code path
- [ ] **D4:** ghaus-fsd — Create `tests/test_webhook_signature_contract.py` for INTAKE with 14+ golden fixture tests

### Must-have (Environment)
- [ ] Deploy all 5 services to staging from the recorded commits
- [ ] Apply all migrations to staging Supabase Postgres
- [ ] Seed test tenants, identities, and webhook secrets
- [ ] Confirm all services pass health checks
- [ ] Verify correlation ID pipeline (SigNoz)

### Must-execute (QA)
- [ ] Re-run all per-service test gates after fixes
- [ ] Execute full Phase 1 primary lifecycle end-to-end
- [ ] Execute Phase 2 webhook security matrix (48 scenarios)
- [ ] Execute Phase 3 idempotency chain
- [ ] Execute Phase 4 contract/schema validation
- [ ] Execute Phase 5-20 as applicable
- [ ] Independent QA agent must report evidence for all executed phases

### Should-fix (Severity 3)
- [ ] **D2:** ghous-isb — Fix SaaS Admin secondary key test cache issue
- [ ] **D5:** yasha — Install `reportlab` dependency for TRACE test environment
- [ ] Clean SaaS Admin untracked files or commit them
- [ ] Register Client Portal in release snapshot or explicitly defer

---

## Final Verdict

```text
RECOMMENDATION: NOT APPROVED
```

Three severity-2 defects remain open. No staging environment exists. The primary lifecycle has never been executed end-to-end. The evidence base is limited to static code analysis and RETAINER's unit tests only.

The architecture review confirms that the binding trust-domain decisions are correctly encoded in the code (portal scope ownership, activation authority, contract registry). However, security implementation defects D1 and D3 prevent controlled-pilot approval.

The product owner (Yasha) makes the final pilot decision after receiving this recommendation.

---

## Appendix: Owner Assignments

| Defect | Service | Owner | Agent |
|--------|---------|-------|-------|
| D1 | SaaS Admin | ghous-isb | admin-agent |
| D3 | RETAINER | ghaus-fsd | retainer-agent |
| D4 | INTAKE | ghaus-fsd | intake-agent |
| D2 | SaaS Admin | ghous-isb | admin-agent |
| D5 | TRACE | yasha | trace-agent |
| ENV | All services | yasha (CTO) | orchestrator |
