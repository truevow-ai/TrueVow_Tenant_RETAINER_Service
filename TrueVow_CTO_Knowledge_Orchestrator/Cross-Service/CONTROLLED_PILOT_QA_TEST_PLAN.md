# TrueVow Cross-Service Controlled Pilot — QA Test Plan v2

**Issued by:** CTO Orchestrator
**Date:** 2026-07-31
**Status:** READY PENDING ENVIRONMENT AND REPOSITORY FREEZE

> QA execution begins only after:
> - Every repository is clean.
> - Every required artifact is committed or deliberately excluded.
> - Staging services are deployed from the recorded commits.
> - Migration revisions are verified.
> - Health checks pass.

---

## Release Candidate Snapshot v2

| # | Service | Branch | Commit SHA | State |
|---|---------|--------|------------|-------|
| 1 | INTAKE (Tenant Application) | main | `5e44f93` | CLEAN |
| 2 | RETAINER | master | `28a9ea4` | CLEAN (service code) |
| 3 | SaaS Admin (Shared Platform) | main | `88d4c2e` | DIRTY (4 untracked helper files) |
| 4 | TRACE | main | `3eb936c` | CLEAN |
| 5 | Customer Portal | master | `29d3edc` | CLEAN |
| 6 | Client Portal | — | — | **NOT RECORDED** — API-simulated in this release; browser-level approval out of scope |

### Migration Revisions
| Service | Revision |
|---------|----------|
| SaaS Admin | `174_portal_architecture.sql` |
| RETAINER | `0008_grant_reference_fields` |
| TRACE | `0017_phase2_schema.py` |
| INTAKE | `20251205000001_api_gateway_audit_log.sql` |

### Webhook Keys (per-caller, per-receiver, per-path, per-method)
| Link | Key IDs |
|------|---------|
| INTAKE → RETAINER | `tv-intake-to-retainer-v1`, `tv-intake-to-retainer-v2` |
| RETAINER → SaaS Admin | `tv-retainer-to-saas-admin-v1` |
| SaaS Admin → TRACE | `tv-saas-admin-to-trace-v1` |

### Signed-Route Query-String Policy (clarified)
> The HMAC signing input excludes the query string. Signed webhook routes prohibit query parameters entirely. A request containing a query string is rejected before business processing with `QUERY_STRING_NOT_ALLOWED`. Do not classify as an ordinary signature mismatch when the signature itself is otherwise valid.

---

## Preparation (Mandatory — QA Agent must verify before testing)

### P0. Environment Sanity
- [ ] All 6 services reachable at listen ports: INTAKE (3022), RETAINER (3038), SaaS Admin (3001), TRACE (3036), Customer Portal (3031), Client Portal (—)
- [ ] `GET /health` returns 200 on all services
- [ ] Staging Supabase Postgres connection confirmed (NOT SQLite)
- [ ] All migrations applied to staging DB
- [ ] Test tenant A and tenant B created with distinct firm IDs
- [ ] Test identities available: staff, attorney, firm-admin, client, unauthorized-user
- [ ] Webhook secrets configured per service relationship (NOT one global secret)
- [ ] Correlation ID generation available and logged end-to-end
- [ ] SigNoz at http://localhost:3301 receiving traces

### P1. Per-Service Test Suite Gate
Before cross-service testing, each service must pass its own webhook signature golden fixtures:
- [ ] RETAINER: `pytest tests/test_webhook_signature.py` — 15/15 pass (confirmed)
- [ ] TRACE: `pytest tests/test_golden_fixture.py` — 17/17 pass
- [ ] INTAKE: `pytest tests/test_webhook_signature_contract.py` — 14/14 pass
- [ ] SaaS Admin: `npm test -- tests/security/webhook-signature.test.ts` — 16/16 pass
- [ ] Customer Portal: `npm test -- tests/contracts/` — pass

---

## Phase 1: Primary Happy-Path Lifecycle

> Capture correlation_id, candidate_id, engagement_id, package_id, activation_command_id, matter_id, `matter.activated` event_id, TRACE matter reference, portal access-grant_id, RETAINER local projection reference.

### 1.1 INTAKE → RETAINER: Candidate Submission
- [ ] INTAKE creates candidate for test tenant
- [ ] INTAKE signs `candidate-submitted` webhook with `tv-intake-to-retainer-v1`
- [ ] RETAINER verifies signature with raw body hash
- [ ] RETAINER stores candidate idempotently
- [ ] RETAINER records correlation_id in audit timeline

### 1.2 Attorney Review & Approval
- [ ] Candidate appears in review queue (attorney identity)
- [ ] Attorney reviews candidate details
- [ ] Attorney approves representation
- [ ] Conflict search initiates
- [ ] Conflict search completes
- [ ] Attorney records conflict clearance

### 1.3 Engagement Package
- [ ] RETAINER resolves approved template
- [ ] Engagement package generates
- [ ] Preflight validation passes
- [ ] Delivery authorized
- [ ] Shared Platform creates engagement access (PROSPECTIVE_ENGAGEMENT scope)
- [ ] Client portal token generated

### 1.4 Signature Ceremony
- [ ] Client receives and reviews package
- [ ] Client records consent
- [ ] Client signs
- [ ] Required firm signature completes
- [ ] Completed copy delivered
- [ ] Package document hash locked

### 1.5 Activation
- [ ] RETAINER activation checklist passes
- [ ] RETAINER signs `ActivateMatterCommand` with `tv-retainer-to-saas-admin-v1`
- [ ] SaaS Admin verifies webhook signature
- [ ] SaaS Admin validates activation evidence
- [ ] SaaS Admin activates Matter (canonical record)
- [ ] SaaS Admin emits signed `matter.activated` with `tv-saas-admin-to-trace-v1`
- [ ] TRACE verifies signature
- [ ] TRACE creates Matter context (no duplicate Matter)
- [ ] Shared Platform adds ACTIVE_MATTER access (MATTER_VIEW, MATTER_MESSAGE, MATTER_UPLOAD, REQUEST_RESPOND, DOCUMENT_DOWNLOAD)
- [ ] RETAINER transitions to ENGAGEMENT_HISTORY only
- [ ] Customer Portal displays TRACE Matter link
- [ ] Same client identity accesses TRACE functionality

---

## Phase 2: Webhook Security — Full Matrix (48 scenarios)

> Run ALL 16 scenarios for EVERY receiving service (RETAINER, SaaS Admin, TRACE).
> Query strings are rejected with `QUERY_STRING_NOT_ALLOWED` before business processing (not SIGNATURE_MISMATCH).

### 2.1 RETAINER Webhook Security (receiver of INTAKE events)

| # | Test | Expected |
|---|------|----------|
| 1 | Valid primary key (`tv-intake-to-retainer-v1`) | 200/202 |
| 2 | Valid secondary rotation key (`tv-intake-to-retainer-v2`) | 200/202 |
| 3 | Missing all signature headers | 401 MISSING_HEADERS |
| 4 | Unknown key_id | 401 UNKNOWN_KEY_ID |
| 5 | Modified body (tampered payload) | 401 SIGNATURE_MISMATCH |
| 6 | Wrong HTTP method (GET instead of POST) | 401 |
| 7 | Wrong canonical path | 401 |
| 8 | Trailing-slash mismatch (`/path/`) | 401 |
| 9 | Query-string in path | 401 QUERY_STRING_NOT_ALLOWED |
| 10 | Malformed timestamp (non-numeric) | 401 MALFORMED_TIMESTAMP |
| 11 | Timestamp older than 300s | 401 EXPIRED_TIMESTAMP |
| 12 | Timestamp in the future (>300s from now) | 401 EXPIRED_TIMESTAMP |
| 13 | Invalid signature hex length | 401 INVALID_SIGNATURE_FORMAT |
| 14 | Legitimate signature from unauthorized service key (e.g., SETTLE key) | 401 UNKNOWN_KEY_ID |
| 15 | Duplicate event_id replay | 202 idempotent — no duplicate candidate |
| 16 | Disabled old key after rotation to v2 | 401 UNKNOWN_KEY_ID |

### 2.2 SaaS Admin Webhook Security (receiver of RETAINER activation)

| # | Test | Expected |
|---|------|----------|
| 1 | Valid primary key | 200/201 |
| 2 | Valid rotation key | 200/201 |
| 3 | Missing headers | 401 |
| 4 | Unknown key_id | 401 |
| 5 | Modified body | 401 |
| 6 | Wrong method | 401 |
| 7 | Wrong path | 401 |
| 8 | Trailing-slash | 401 |
| 9 | Query-string | 401 QUERY_STRING_NOT_ALLOWED |
| 10 | Non-numeric timestamp | 401 |
| 11 | Expired timestamp | 401 |
| 12 | Future timestamp | 401 |
| 13 | Invalid hex | 401 |
| 14 | Cross-service key (e.g., INTAKE key) | 401 |
| 15 | Duplicate command_id replay | 200 idempotent — no second Matter |
| 16 | Disabled old rotation key | 401 |

### 2.3 TRACE Webhook Security (receiver of SaaS Admin matter.activated)

| # | Test | Expected |
|---|------|----------|
| 1 | Valid primary key | 200/201 |
| 2 | Valid rotation key | 200/201 |
| 3 | Missing headers | 401 |
| 4 | Unknown key_id | 401 |
| 5 | Modified body | 401 |
| 6 | Wrong method | 401 |
| 7 | Wrong path | 401 |
| 8 | Trailing-slash | 401 |
| 9 | Query-string | 401 QUERY_STRING_NOT_ALLOWED |
| 10 | Non-numeric timestamp | 401 |
| 11 | Expired timestamp | 401 |
| 12 | Future timestamp | 401 |
| 13 | Invalid hex | 401 |
| 14 | Legitimate signature from unauthorized service | 401 |
| 15 | Duplicate event_id replay | 200 idempotent — no duplicate TRACE Matter |
| 16 | Disabled old rotation key | 401 |

### 2.4 Raw Body Verification
- [ ] Confirm raw bytes are hashed (NOT JSON-reserialized)
- [ ] Confirm body SHA matches between sender and receiver for identical raw bytes
- [ ] Confirm re-serializing JSON to different key order produces different signature

---

## Phase 3: Full Idempotency Chain

### 3.1 INTAKE → RETAINER
- [ ] Replay same `event_id` with identical payload → 202, same workflow_id
- [ ] Replay same `event_id` with different payload hash → 409 CONFLICT
- [ ] Event_id replay recorded in audit evidence
- [ ] No duplicate candidate row in DB

### 3.2 RETAINER → SaaS Admin
- [ ] Replay same `command_id` → 200, same activation result
- [ ] No second Matter created
- [ ] No duplicate activation side effects (no double portal grants)

### 3.3 SaaS Admin → TRACE
- [ ] Replay same `matter.activated` event_id → 200 idempotent
- [ ] No duplicate TRACE Matter
- [ ] Existing Matter context preserved and linked
- [ ] No duplicate portal permissions added

### 3.4 Concurrent Idempotency (Addendum A5)
For each hop, send at least 10 concurrent identical deliveries:
- [ ] INTAKE → RETAINER: exactly one canonical row, one state transition, one downstream event
- [ ] RETAINER → SaaS Admin: exactly one activation
- [ ] SaaS Admin → TRACE: exactly one TRACE Matter
- [ ] All other requests receive same existing result or documented idempotent response
- [ ] Database uniqueness constraints enforce result (not only in-memory locks)
- [ ] Same identifier with different payload hash concurrently:
  - [ ] One payload wins according to documented policy
  - [ ] Conflicting payloads rejected
  - [ ] No mixed or partially overwritten state

---

## Phase 4: Contract and Schema-Version Validation (Addendum A4)

For every receiving service, test valid HMAC with invalid business contract:

- [ ] Unsupported `schema_version` → 400/422, auth succeeds, contract validation fails
- [ ] Missing one of 18 required EventEnvelope fields → 400/422
- [ ] Unknown event type → 400/422
- [ ] Wrong producer service → 400/422
- [ ] Wrong consumer service → 400/422
- [ ] Wrong tenant identifier → 400/422
- [ ] Invalid command or event identifier → 400/422
- [ ] Invalid payload schema → 400/422
- [ ] Extra prohibited fields → 400/422
- [ ] Valid envelope with invalid embedded command → 400/422

**Expected:** Authentication succeeds. Contract validation fails with 400 or 422. No database or downstream side effect. Rejection audited safely. Authentication and contract validation are independent controls.

---

## Phase 5: Tenant Isolation

> Use Tenant A and Tenant B with deliberately substituted resource IDs.

- [ ] Tenant A cannot read Tenant B candidate → 404 (no info disclosure)
- [ ] Tenant A cannot access Tenant B conflict search → 404
- [ ] Tenant A cannot access Tenant B package → 404
- [ ] Tenant A cannot access Tenant B signature ceremony → 404
- [ ] Tenant A cannot access Tenant B activation checklist → 404
- [ ] Tenant A cannot access Tenant B audit timeline → 404
- [ ] Tenant A cannot access Tenant B Matter → 404
- [ ] Tenant A cannot access Tenant B TRACE requests → 404
- [ ] Tenant A cannot use Tenant B Client Portal token → 401
- [ ] Tenant A cannot access Tenant B documents/uploads → 404
- [ ] Error responses must NOT disclose whether Tenent B's resource exists

---

## Phase 6: Authority & Role Tests

> Use separate identities: staff, attorney, firm-admin, client, unauthorized.

- [ ] Staff cannot approve representation → 403
- [ ] Staff cannot clear conflicts → 403
- [ ] Staff cannot authorize attorney-only delivery → 403
- [ ] Staff cannot authorize activation → 403
- [ ] Firm-admin does NOT automatically get attorney authority → 403
- [ ] Client cannot access attorney endpoints → 403
- [ ] Client cannot access Customer Portal endpoints → 403
- [ ] Unauthorized user cannot access any tenant resources → 401
- [ ] Disabled UI actions cannot be bypassed with direct API calls → 403
- [ ] Product backends are final authority evaluators (not just frontend guards)

---

## Phase 7: Portal Scope Ownership

### 7.1 Pre-Activation
- [ ] Client has PROSPECTIVE_ENGAGEMENT permissions only
- [ ] Client can view engagement package
- [ ] Client can ask questions
- [ ] Client can sign
- [ ] Client can download completed copy

### 7.2 Post-Activation
- [ ] **RETAINER projection:** only `ENGAGEMENT_HISTORY` scope
- [ ] **Shared Platform canonical grant:** `ACTIVE_MATTER` with `MATTER_VIEW, MATTER_MESSAGE, MATTER_UPLOAD, REQUEST_RESPOND, DOCUMENT_DOWNLOAD`
- [ ] RETAINER has `MATTER_*` scopes in its projection → **MUST FAIL (defect if present)**
- [ ] Same client identity retains engagement history access
- [ ] Same client identity retains completed document access
- [ ] Same client identity gains TRACE Matter access
- [ ] Same client identity does NOT require a second account/login
- [ ] Portal access grant upgrade chain intact (`previous_grant_id` links PROSPECTIVE_ENGAGEMENT → ACTIVE_MATTER)

### 7.3 Scope Enforcement
- [ ] Client with ENGAGEMENT_HISTORY cannot use MATTER endpoints → 403
- [ ] Client with ACTIVE_MATTER can use TRACE client portal endpoints
- [ ] TRACE does NOT canonically own Shared Platform access grants
- [ ] RETAINER stores only its local access projection (not canonical)

---

## Phase 8: Client Portal — Browser Scenarios (Addendum A2)

> API-simulated in this release. Browser-level Client Portal approval is out of scope.

Required browser-level scenarios when Client Portal is available:

- [ ] Invitation acceptance
- [ ] Client identity verification
- [ ] Package review
- [ ] Electronic consent
- [ ] Client question submission
- [ ] Signature-session launch
- [ ] Completed-copy download
- [ ] Post-activation engagement-history access
- [ ] Same-account TRACE Matter access
- [ ] Logout and session revocation
- [ ] Expired invitation handling
- [ ] Revoked access handling

**Gate:** A controlled pilot involving real clients must not be approved using API simulation alone.

---

## Phase 9: Customer Portal Browser Validation (Addendum A14)

- [ ] Clerk login
- [ ] Tenant switching restrictions
- [ ] RETAINER entitlement visibility
- [ ] Candidate list and pagination
- [ ] Candidate detail
- [ ] Stale-version blocking
- [ ] Attorney-only actions
- [ ] Conflict terminology
- [ ] Package preflight and authorization
- [ ] Client Activity display
- [ ] Nine-item activation checklist
- [ ] TRACE link appearance after activation
- [ ] Direct URL and API attempts cannot bypass disabled UI controls

---

## Phase 10: Failure & Reconciliation Paths

- [ ] INTAKE unavailable during Customer Portal enrichment → graceful degradation, no data loss
- [ ] Stale candidate version → rejected, retry with fresh version
- [ ] Representation decline → DECLINED_OR_EXPIRED
- [ ] Representation defer → stays NOT_STARTED, later approved
- [ ] Conflict hold → CONFLICT_HOLD, package prep blocked
- [ ] Conflict source unavailable → hold, retry, eventual clearance
- [ ] Package preflight failure → generation blocked
- [ ] Package expiration → DECLINED_OR_EXPIRED
- [ ] Signature invalidation → returns to SIGNATURE_PENDING
- [ ] Client decline → DECLINED_OR_EXPIRED
- [ ] Completed-copy delivery failure → retry, eventual delivery
- [ ] Activation timeout → uncertain state, retry idempotently
- [ ] Activation uncertain → reconciliation check, no double-activation
- [ ] Activation reconciliation → recovers to consistent state
- [ ] TRACE temporarily unavailable → retry, eventual consumption, idempotent
- [ ] Portal access synchronization failure → reconcilable, no orphan grants
- [ ] **No service may invent success after a timeout or incomplete response**

---

## Phase 11: Retry and Delivery Behavior (Addendum A13)

Transient failures at every hop:

- [ ] Receiver unavailable → bounded exponential backoff
- [ ] Connection timeout → retry, no duplicate state
- [ ] HTTP 500 → retry, no duplicate state
- [ ] HTTP 429 → bounded backoff
- [ ] Database temporarily unavailable → retry
- [ ] Sender restart after delivery but before acknowledgement → idempotent replay
- [ ] Permanent 4xx errors NOT retried indefinitely
- [ ] Exhausted deliveries enter observable reconciliation or dead-letter state
- [ ] Recovery does not require manually editing canonical records

---

## Phase 12: Raw-Body and Transport Edge Cases (Addendum A6)

- [ ] Empty body
- [ ] Whitespace-only body
- [ ] UTF-8 non-ASCII content
- [ ] Different JSON key ordering (same semantic payload)
- [ ] Duplicate JSON keys
- [ ] Additional trailing newline
- [ ] Invalid UTF-8 → rejected
- [ ] Wrong `Content-Type` → rejected
- [ ] Compressed request body → rejected or handled per contract
- [ ] Body exceeding configured size limit → rejected
- [ ] Chunked transfer (where supported)

Sender and receiver must hash the same exact raw bytes.

---

## Phase 13: Key Rotation Operational Test (Addendum A7)

1. [ ] Receiver accepts primary v1
2. [ ] Receiver configured to accept v1 and v2
3. [ ] Sender changes to v2
4. [ ] Requests signed by v2 pass
5. [ ] Receiver disables v1
6. [ ] Requests signed by v1 fail
7. [ ] Services restart and retain correct key configuration
8. [ ] No shared or unrelated service key accepted
9. [ ] INTAKE-to-RETAINER key cannot authenticate to SaaS Admin
10. [ ] INTAKE-to-RETAINER key cannot authenticate to TRACE
11. [ ] RETAINER-to-SaaS Admin key cannot authenticate to TRACE

Record only key IDs and configuration fingerprints, never secrets.

---

## Phase 14: Legacy Authentication Cutoff (Addendum A8)

For RETAINER's temporary legacy authentication path:

### Before September 1, 2026 (injectable clock)
- [ ] Legacy bearer accepted only where migration policy permits
- [ ] Deprecation warning and metric recorded
- [ ] HMAC remains preferred

### On and after September 1, 2026
- [ ] Legacy bearer rejected
- [ ] HMAC continues to work
- [ ] No manual deployment change required to enforce cutoff
- [ ] Rejection does not fall back silently

---

## Phase 15: Database Validation (Staging Postgres only)

- [ ] SaaS Admin migrations 169-174 applied
- [ ] `contract_registry` table populated with 12+ contracts
- [ ] `contract_golden_fixtures` table has golden-matter-activated-v1 and golden-envelope-v1
- [ ] `matter_activations` table exists (migration 170)
- [ ] `client_portal_access_grants` table exists (migration 174)
- [ ] `fn_upgrade_portal_access_on_activation` trigger compiles
- [ ] RETAINER alembic head at `0008_grant_reference_fields`
- [ ] RETAINER schema tables exist in `retainer` schema
- [ ] TRACE alembic head at `0017_phase2_schema.py`
- [ ] All foreign keys resolve
- [ ] Tenant constraints exist on multi-tenant tables
- [ ] Unique/idempotency constraints exist on event_id, command_id columns
- [ ] RLS active where required

---

## Phase 16: RLS Role Validation (Addendum A11)

Test access using actual database roles:

- [ ] Tenant A cannot retrieve Tenant B rows via anon/client role
- [ ] Tenant A cannot retrieve Tenant B rows via authenticated tenant role
- [ ] Service-role access limited to intended services
- [ ] Direct database access cannot bypass application tenant checks
- [ ] New tables do not inherit permissive policies
- [ ] Views and functions use safe security-definer behavior where applicable
- [ ] TRACE does NOT canonically own Shared Platform access grant records
- [ ] RETAINER stores only its local access projection

---

## Phase 17: Migration Safety and Rollback (Addendum A10)

Before applying staging migrations:

- [ ] Capture database backup or restorable snapshot
- [ ] Record migration checksums
- [ ] Record expected locking behavior
- [ ] Record whether backfill is required
- [ ] Verify migration ordering
- [ ] Verify migrations are safe to rerun or fail clearly

After migration:

- [ ] Run schema smoke tests
- [ ] Compare expected tables, indexes, constraints, triggers, RLS, functions
- [ ] Verify application startup

Test rollback or forward-fix in disposable Postgres environment. Do not test destructive rollback against shared staging data.

---

## Phase 18: Release Artifact Integrity (Addendum A1)

Before QA begins, record for every service:

- [ ] Repository commit SHA
- [ ] Clean working-tree result
- [ ] Container image digest or deployment artifact hash
- [ ] Lockfile hash
- [ ] Migration file checksum
- [ ] OpenAPI or contract hash
- [ ] Deployment configuration version

QA must test deployed artifacts built from the recorded commits. Running services from mutable local working directories is not acceptable release evidence. Any code, migration, dependency, or configuration change during QA invalidates the frozen release snapshot.

---

## Phase 19: Observability Acceptance (Addendum A12)

For the primary lifecycle, verify one correlation chain across every service:

Capture:
- [ ] Correlation ID
- [ ] Event or command ID
- [ ] Producer service
- [ ] Consumer service
- [ ] Attempt number
- [ ] Delivery latency
- [ ] Verification result
- [ ] Idempotency result
- [ ] Final state

Confirm:
- [ ] SigNoz receives the complete chain
- [ ] Logs contain no webhook secret
- [ ] Logs contain no full signature
- [ ] Logs contain no access token
- [ ] Logs contain no prohibited PII or PHI
- [ ] Retries and failures are visible
- [ ] Dead-letter or reconciliation paths are observable
- [ ] End-to-end event propagation within acceptable threshold

---

## Phase 20: Test-Data Cleanup (Addendum A15)

After QA:

- [ ] Revoke all temporary webhook keys
- [ ] Revoke test Client Portal sessions and invitations
- [ ] Remove or archive test tenants according to policy
- [ ] Mark test Matters and candidates as synthetic
- [ ] Remove test documents from client-facing storage
- [ ] Preserve non-sensitive QA evidence
- [ ] Confirm no synthetic notification reaches a real recipient

---

## Severity Classification (Addendum A16)

### Severity 1 (BLOCKS pilot approval)
- Cross-tenant exposure
- Authentication or signature bypass
- Duplicate canonical Matter
- Incorrect legal-authority action
- Missing or corrupt canonical data
- Staging environment or database unavailable
- Secret exposure

### Severity 2 (BLOCKS pilot approval)
- Main lifecycle cannot complete
- Portal scope ownership incorrect
- Required evidence missing
- Idempotency failure without confirmed data corruption
- Completed copy unavailable
- Reconciliation cannot recover automatically

### Severity 3 (Does not block)
- Noncritical UI defect
- Incorrect non-authoritative label
- Recoverable operational inconvenience
- Minor observability gap

**No Severity 1 or Severity 2 defect may remain open for controlled-pilot approval.**

---

## Evidence Collection Protocol

For every test case, QA agent must capture:
- Test name and number
- PASS / FAIL
- Correlation ID
- HTTP status code
- Response body DTO keys (no secrets, no PHI)
- DB row counts before/after (where applicable)
- Any error or unexpected behavior

---

## Final Approval Separation (Addendum A17)

The independent QA agent executes and records the test evidence.

The CTO Orchestrator:
- Reviews evidence
- Validates architecture
- Assigns defects
- Confirms retests
- Issues a recommendation

The product owner provides the final approval.

**The service agent that implements a fix may not be the sole validator of that fix.**

---

## Override Rules for QA Agent

1. **Do not modify application code.** Report defects; do not fix.
2. **Do not modify webhook contracts** to make tests pass.
3. **Use staging Postgres only.** SQLite results are NOT evidence.
4. **Never include secrets, access tokens, complete signatures, or PHI in the report.**
5. **If a service is unreachable, report it as a severity-1 defect.**
6. **If staging Postgres migrations are incomplete, report it as a severity-1 defect.**
7. **Produce raw evidence — do not explain away failures.**
8. **Services must be deployed from recorded commits. Mutable local directories are not valid release evidence.**

---

## Final Recommendation Template

```text
APPROVED FOR CONTROLLED PILOT
CONDITIONALLY APPROVED
NOT APPROVED
```

**Approval requires ALL of:**
- Complete happy-path lifecycle passes
- All webhook security tests pass (48 scenarios — 16 per receiver x 3 receivers)
- All idempotency tests pass (sequential + concurrent)
- Contract/schema-version validation passes (10 scenarios per receiver)
- Tenant isolation passes (11 scenarios)
- Authority controls pass (10 scenarios)
- Correct portal-scope ownership proven (no MATTER_* in RETAINER)
- Raw-body edge cases handled (11 scenarios)
- Key rotation test passes
- Legacy cutoff enforced
- No unresolved severity-1 or severity-2 defects
- Staging Postgres migrations confirmed applied
- RLS role validation passes
- Migration safety and rollback confirmed
- Release artifact integrity recorded
- Observability chain complete
- TRACE receives canonical activated Matter successfully
- Client Portal browser scenarios completed or explicitly deferred
