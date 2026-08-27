# Controlled Cross-Service Pilot Validation — Release Freeze

**Frozen by:** CTO Orchestrator (Yasha)
**Date:** 2026-07-31
**Status:** FREEZE IN PROGRESS — BLOCKERS IDENTIFIED

---

## 1. Release Candidate Commit Snapshot

| # | Service | Product Name | Repo Path | Branch | Commit SHA | Git State | Last Commit Message |
|---|---------|-------------|-----------|--------|------------|-----------|-------------------|
| 1 | INTAKE | Tenant Application | `TrueVow_Tenant_Application_Service` | main | `a039afd` | **CLEAN** | feat(security): WebhookSignature v1.0 golden fixture tests — 14/14 pass |
| 2 | RETAINER | Tenant RETAINER | `TrueVow_Tenant_RETAINER_Service` | master | `2d66444` | **DIRTY** (2 files deleted, docs modified, memory.db staged) | memory(Admin): Webhook Key Mapping |
| 3 | SaaS Admin | Shared Platform | `TrueVow_SaaS_Administration_Service` | main | `88d4c2e` | **DIRTY** (3 untracked SQL helper files) | security: per-service key isolation — separate keys per caller-receiver pair |
| 4 | TRACE | Tenant TRACE | `TrueVow_Tenant_TRACE_Service` | main | `3eb936c` | **CLEAN** | docs(trace): enforce per-link webhook keys and contract source pinning |
| 5 | Customer Portal | Tenant Portal | `Truevow_Tenant_Customer_Portal_Service` | master | `29d3edc` | **CLEAN** | security(contracts): per-link key isolation — NO global shared secret |

## 2. Database Migration Revisions

| Service | Migration System | Revision/Migration Head | Files |
|---------|-----------------|------------------------|-------|
| INTAKE | Raw SQL (no Alembic) | `20251205000001_api_gateway_audit_log.sql` | 3 SQL files in `supabase/migrations/` |
| RETAINER | Alembic (async) | `0008_grant_reference_fields` | 8 revisions in `infra/database/migrations/versions/` |
| SaaS Admin | Manual SQL (Supabase) | `174_portal_architecture.sql` | 95+ numbered migrations 003-174 |
| TRACE | Alembic (dual-engine) | `0017_phase2_schema.py` | 17 revisions in `infra/database/migrations/versions/` |
| Customer Portal | N/A (frontend-only Next.js service) | — | — |

### Key SaaS Admin Migration Chain
- `169_contract_normalization.sql` → `contract_registry` table
- `170_retainer_activation_contract.sql` → `matter_activations` table
- `173_final_contract_fixes.sql` → `contract_golden_fixtures` table + 2 seeded fixtures
- `174_portal_architecture.sql` → `client_portal_access_grants`, `client_portal_invitations`, `communication_threads`, `tenant_branding_config`, `fn_upgrade_portal_access_on_activation` trigger

## 3. Webhook Key Registry (per-service isolation)

| Caller → Receiver | Key ID(s) | HTTP Method | Canonical Path | Rotation |
|-------------------|-----------|-------------|----------------|----------|
| INTAKE → RETAINER | `tv-intake-to-retainer-v1`, `tv-intake-to-retainer-v2` | POST | `/api/v1/retainer/webhooks/candidate-submitted` | v1 primary, v2 rotation |
| RETAINER → SaaS Admin | `tv-retainer-to-saas-admin-v1` | POST | `/api/v1/matters/activate` | Single key |
| SaaS Admin → TRACE | `tv-saas-admin-to-trace-v1` (per contract) | POST | `/api/v1/trace/webhooks/matter-activated` | Needs confirmation |

**WebhookSignature v1.0 Canonical Contract (frozen, shared by all services):**
- Algorithm: HMAC-SHA256
- Signing string: `{timestamp_ms}:{METHOD}:{path}:{body_sha256}`
- Headers: `X-TrueVow-Key-Id`, `X-TrueVow-Timestamp`, `X-TrueVow-Signature`
- Replay window: 300,000 ms (5 minutes)
- Hash: raw bytes, not JSON-reserialized
- Signature hex length: 64 characters
- Timing-safe comparison: `hmac.compare_digest`

**Confirmed: NO global platform-wide shared secret.** Each relationship uses its own key.

## 4. Staging Environment Status (as of freeze)

| Item | Status |
|------|--------|
| Docker deployment | **NOT_DEPLOYED** |
| Supabase Postgres (staging) | **NOT CONFIRMED RUNNING** |
| Services running locally | **NOT CONFIRMED** |
| Test tenants/users seeded | **NOT CONFIRMED** |
| Correlation ID pipeline | **NOT CONFIRMED** |
| Log aggregation (SigNoz) | Available at http://localhost:3301 |

**Gate condition: Staging services must be started and confirmed healthy before QA execution begins.**

## 5. Blockers — Must Resolve Before QA Handoff

### BLOCKER 1: RETAINER Dirty State
RETAINER has uncommitted deletions that affect production security code:
- `app/security/__init__.py` — deleted (old docstring, replaced by new module)
- `app/security/webhook_auth.py` — deleted (old webhook auth, migrated to `webhook_signature.py`)

**Action required:** RETAINER owner (ghaus-fsd) must commit these deletions OR revert them.
**Rationale:** No unrecorded changes during testing. These files were deleted as part of the WebhookSignature v1.0 migration. The new `webhook_signature.py` already exists committed.

### BLOCKER 2: SaaS Admin Dirty State
SaaS Admin has 3 untracked files:
- `supabase/RUN_ME_MANUALLY.sql`
- `supabase/SAAS_ADMIN_DB_ONLY.sql`
- OpenCode tool output script

**Action required:** SaaS Admin owner (ghous-isb) must either commit, remove, or .gitignore these files.

### BLOCKER 3: Staging Environment Availability
No services are confirmed running. The pilot requires:
- All 5 services healthy and listening
- Staging Supabase Postgres with migrations applied
- Test tenants, users, and identities seeded
- Correlation ID pipeline operational

## 6. Contract Registry & Golden Fixtures (pre-verified)

| Artifact | Location | Status |
|----------|----------|--------|
| `contract_registry` table | SaaS Admin migration 169 | Schema exists in SQL |
| `contract_golden_fixtures` table | SaaS Admin migration 173 | Schema exists in SQL; 2 fixtures seeded |
| `golden-matter-activated-v1` | SaaS Admin migration 173 | 18-field EventEnvelope v1.0.1 |
| `golden-envelope-v1` | SaaS Admin migration 173 | Generic envelope conformance |
| RETAINER golden fixture tests | `tests/test_webhook_signature.py` | 16/16 pass (per last commit) |
| TRACE golden fixture tests | `tests/test_golden_fixture.py` | 17/17 pass (per last commit) |
| INTAKE golden fixture tests | `tests/test_webhook_signature_contract.py` | 14/14 pass (per last commit) |
| SaaS Admin golden fixture tests | `tests/security/webhook-signature.test.ts` | 16/16 pass (per last commit) |
| Customer Portal golden fixture tests | Part of TRACE contract module | Present |
| SETTLE golden fixture tests | Enumerated in scan report | 17 pass |

**All services share the same WebhookSignature v1.0 contract and compute the same HMAC over identical golden fixtures.**

## 7. Architecture & Authority Baseline (binding, from canonical-decisions.md)

These are the invariants the architecture review will verify:

- INTAKE owns intake and candidate submission
- RETAINER owns engagement and activation preparation; transitions only to `ENGAGEMENT_HISTORY`
- SaaS Admin is canonical Matter activation authority
- TRACE consumes canonical `matter.activated` without duplicating Matter
- Shared Platform (SaaS Admin) owns client identity and cross-product access grants
- RETAINER **never** grants `MATTER_*` scopes
- Shared Platform adds `ACTIVE_MATTER` with `MATTER_VIEW, MATTER_MESSAGE, MATTER_UPLOAD, REQUEST_RESPOND, DOCUMENT_DOWNLOAD`
- Webhook keys restricted by caller, receiver, path, method, environment
- All events and commands are idempotent
- Auth = Clerk 3-domain; no Supabase Auth
- `case_id` only minted by SaaS Admin MDM
- No direct cross-product database writes

## 8. Owner Assignments

| Service | Owner | Agent | Contact |
|---------|-------|-------|---------|
| INTAKE | ghaus-fsd | intake-agent | Ghulam Ghaus |
| RETAINER | ghaus-fsd | retainer-agent | Ghulam Ghaus |
| SaaS Admin | ghous-isb | admin-agent | Ghulam Ghous |
| TRACE | yasha | trace-agent | Yasha |
| Customer Portal | yasha | portal-agent | Yasha |

## 9. Next Steps

1. **Yasha (CTO Orchestrator):** Produce controlled pilot test plan → handoff to QA
2. **ghaus-fsd:** Commit RETAINER webhook_auth.py deletions
3. **ghous-isb:** Clean SaaS Admin untracked files
4. **CTO Orchestrator:** Confirm staging environment; coordinate service startup
5. **CTO Orchestrator:** Re-freeze after blockages cleared
6. **Independent QA Agent:** Execute full test plan
7. **Service agents:** Fix defects (own service only)
8. **Independent QA Agent:** Rerun affected + regression tests
9. **CTO Orchestrator (Architecture Reviewer):** Architecture and release review
10. **Yasha (Product Owner):** Final APPROVE / CONDITIONAL / REJECT decision
