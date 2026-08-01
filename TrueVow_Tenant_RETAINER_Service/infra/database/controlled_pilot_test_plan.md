# RETAINER Controlled Pilot Test Plan v1.0

## Pre-flight

- [ ] RETAINER working tree clean (SHA: ________________)
- [ ] SaaS Admin working tree clean (SHA: ________________)
- [ ] INTAKE working tree clean (SHA: ________________)
- [ ] TRACE working tree clean (SHA: ________________)
- [ ] Staging env vars configured (per-service keys, NOT global shared secret)
- [ ] All services running: INTAKE (3021), RETAINER (3038), SaaS Admin (3001), TRACE
- [ ] `health` endpoints return 200 on all services

## Phase 1: Webhook Spine — HMAC v1.0

### 1.1 INTAKE → RETAINER candidate handoff
- [ ] INTAKE signs with `tv-intake-to-retainer-v1`
- [ ] RETAINER verifies and imports candidate
- [ ] Duplicate `event_id` returns idempotent (202, same workflow_id)
- [ ] Conflicting `event_id` (different hash) returns 409

### 1.2 RETAINER → SaaS Admin activation
- [ ] RETAINER signs `ActivateMatterCommand` with `tv-retainer-to-saas-admin-v1`
- [ ] SaaS Admin verifies and activates Matter
- [ ] Duplicate `command_id` returns idempotent result

### 1.3 SaaS Admin → TRACE matter.activated
- [ ] SaaS Admin signs with `tv-saas-admin-to-trace-v1`
- [ ] TRACE verifies and creates Matter context
- [ ] Duplicate event does not create duplicate TRACE Matter

### 1.4 Negative HMAC tests
- [ ] Correct signature with wrong path → rejected
- [ ] Correct signature from unauthorized caller key → rejected
- [ ] Expired timestamp (301s old) → rejected
- [ ] Just-valid timestamp (299s old) → accepted
- [ ] Primary-to-secondary key rotation → accepted with new key
- [ ] Old key disabled after rotation → rejected
- [ ] Legacy bearer token → rejected after 2026-09-01 cutoff

## Phase 2: Full Lifecycle — Happy Path

- [ ] INTAKE → RETAINER: candidate submitted
- [ ] RETAINER: candidate appears in review queue
- [ ] RETAINER: attorney starts review, approves representation
- [ ] RETAINER: conflict search runs, attorney clears
- [ ] RETAINER: template resolves, package generates
- [ ] RETAINER: delivery authorized, portal token generated
- [ ] RETAINER: ceremony created, signatures applied, fully executed
- [ ] RETAINER: activation checklist created, attorney authorizes
- [ ] RETAINER → SaaS Admin: matter activated
- [ ] SaaS Admin → TRACE: matter.activated consumed
- [ ] TRACE: Matter context created, linked to same client identity
- [ ] RETAINER: client access becomes ENGAGEMENT_HISTORY
- [ ] Shared Platform: adds ACTIVE_MATTER after matter.activated
- [ ] Client Portal: engagement history readable, no MATTER_* scopes from RETAINER

## Phase 3: Alternative Paths

- [ ] Representation declined → DECLINED_OR_EXPIRED
- [ ] Representation deferred → stays NOT_STARTED, later approved
- [ ] Missing information requested → request items created, submitted, verified
- [ ] Conflict hold applied → CONFLICT_HOLD, package prep blocked
- [ ] Conflict search invalidated by party change → re-search required
- [ ] Package preflight fails → generation blocked
- [ ] Signature invalidated → returns to SIGNATURE_PENDING
- [ ] Required signer incomplete → mark-executed blocked
- [ ] Client decline → DECLINED_OR_EXPIRED
- [ ] Engagement expired → DECLINED_OR_EXPIRED

## Phase 4: Security & Authority

- [ ] Staff cannot approve representation → 403
- [ ] Staff cannot clear conflicts → 403
- [ ] AI/system actor cannot approve → 403
- [ ] Cross-tenant candidate access → 404
- [ ] Cross-tenant package access → 404
- [ ] Cross-tenant portal token access → 404
- [ ] Client portal invalid token → 401
- [ ] Client portal cross-engagement access → 403
- [ ] No internal fields in client API responses (exact-key DTO allowlist)

## Phase 5: Post-Activation

- [ ] ENGAGEMENT_HISTORY scope → read endpoints still accessible
- [ ] Client decline rejected after activation → 403
- [ ] Client questions rejected after activation → 403
- [ ] Completed copy downloadable after activation
- [ ] Documents readable after activation
- [ ] Signature history readable after activation
- [ ] No MATTER_* scopes in RETAINER projection

## Phase 6: Audit & Evidence

- [ ] Audit timeline includes all major transitions
- [ ] TRACE manifest generated correctly
- [ ] Engagement outcome recordable with evidence classification
- [ ] Client experience projection buildable per workflow state

## Phase 7: Reproducibility

- [ ] Checkout each service at recorded SHA
- [ ] Apply migrations
- [ ] Run service-level test suites
- [ ] All static gates pass (TypeScript, ESLint, ruff, build)
- [ ] Staging deployment matches commit SHAs exactly
