# Phase 4 — Consumer Contract Certification

**Phase:** 4 of 5
**Authority:** CTO-Knowledge-Orchestrator (certification only)
**Prerequisite:** Phase 3 approval

---

## Decision

**CONDITIONAL CERTIFICATION**

Contracts are frozen and schemas published. Cross-repository compatibility is verified at the specification level. Implementation-level verification (TypeScript ↔ Python equivalence, SaaS Admin receiver acceptance) requires the Phase 4 implementation work to complete.

---

## 1. EventEnvelope v1.1.0 Certification

### Specification Status

| Artifact | Status | Location |
|---|---|---|
| JSON Schema v1.1.0 | Frozen | `contracts/event-envelope.schema.json` |
| TypeScript interface | Frozen | `lib/contracts/index.ts` |
| Python model | Implemented | `scripts/events/event_builder.py` |
| Golden fixture (legal) | Seeded | `migration 173` |
| Golden fixture (salesops pre-tenant) | Seeded | `migration 176` |
| Compatibility matrix | Published | `EVENT_ENVELOPE_V1_1_0_COMPATIBILITY_MATRIX.md` |

### Canonical Equivalence Test

```text
Input: { event_type: "salesops.lead.discovered", ... }

TypeScript:  buildPreTenantEvent(params)
Python:      build_pre_tenant_event(**params)

Expected:    canonicalizeForComparison(ts_result) === canonicalize_for_comparison(py_result)
```

Implementation status:
- [ ] TypeScript builder created (`lib/events/event-builder.ts`)
- [ ] Python builder created (`scripts/events/event_builder.py`)
- [ ] Golden fixture test written (same input → same canonicalized output)
- [ ] Field ordering identical in both languages (sorted keys)
- [ ] `tenant_id: null` serialized correctly in both languages
- [ ] `authority_domain: "salesops"` present in both languages
- [ ] Date format identical (ISO 8601 with same precision)

### Consumer Compatibility

| Consumer | v1.1.0 Ready? | Action required |
|---|---|---|
| SaaS Admin | Needs verification | Verify receiver accepts `tenant_id: null`; validate `authority_domain` |
| INTAKE | Backward compatible | `tenant_id` is always non-null for legal-product events |
| RETAINER | Backward compatible | `tenant_id` is always non-null for legal-product events |
| TRACE | Backward compatible | `tenant_id` is always non-null for legal-product events |
| SETTLE | Backward compatible | `tenant_id` is always non-null for legal-product events |

---

## 2. SalesOpsApprovedCustomerHandoff v1.0.0 Certification

### Specification Status

| Artifact | Status | Location |
|---|---|---|
| JSON Schema v1.0.0 | Frozen | `docs/contracts/handoff-contract-v1.0.0.schema.json` |
| Contract registry entry | Registered | `migration 176` |
| Anti-corruption mapping | Published | `SALES_OPS_TO_SAAS_ADMIN_MAPPING.md` |

### Schema Validation Check

| Check | Result |
|---|---|
| No legal-product entities in payload (ENT-xxx) | ✅ Confirmed — all entity refs use `tv.salesops.*` namespace |
| `CustomerCandidate` ≠ `Tenant` | ✅ Confirmed — candidate is input, not the created entity |
| Firm data → ENT-012 Organization | ✅ Defined in mapping |
| Contact data → ENT-014 ContactPoint | ✅ Defined in mapping |
| Approved products → entitlements | ✅ Defined in mapping |
| Authority record included | ✅ Required field |
| Policy version included | ✅ Required field |
| Sensitivity class = INTERNAL_CONFIDENTIAL | ✅ Hard-coded in schema |
| Idempotency key (handoff_id) present | ✅ Required field |
| Checksum present | ✅ Required field |

### Implementation Status

- [ ] SaaS Admin receiver parses handoff payload against this schema
- [ ] Unknown fields rejected (`additionalProperties: false`)
- [ ] Checksum verified before processing
- [ ] `handoff_id` used as idempotency key
- [ ] Organization resolution implemented
- [ ] ContactPoint resolution implemented
- [ ] Tenant creation from handoff implemented
- [ ] Entitlement configuration from approved_products implemented

---

## 3. Webhook Signature Contract Certification

### Specification Status

| Artifact | Status |
|---|---|
| HMAC-SHA256 signing contract | Frozen (WebhookSignature v1.0) |
| Key registry: `tv-sales-ops-to-saas-admin-v1` | Defined |
| Signing string: `timestamp:method:path:bodyHash` | Frozen |
| Headers: `X-TrueVow-Key-Id`, `X-TrueVow-Timestamp`, `X-TrueVow-Signature` | Frozen |
| Replay window: 300,000 ms | Frozen |
| Legacy cutoff: 2026-09-01 | Frozen |
| Sales Ops sender | Implemented (`webhook-client.ts`) |
| SaaS Admin receiver | Implemented (`application-approved/route.ts`) |

### HMAC Cutoff Assurance

| Check | Status |
|---|---|
| API-key fallback cannot occur after 2026-09-01 | [ ] Code enforces date check on legacy fallback path |
| Invalid HMAC never triggers fallback | [ ] Legacy fallback only reached if HMAC headers absent |
| Fallback use is logged and metered | [ ] `console.warn` exists in receiver; no metrics counter yet |
| Alerting begins before cutoff | [ ] No alerting configured |
| Clock-dependent tests use injectable clock | [ ] Not verified |
| Key rotation documented and tested | [ ] Not verified — secondary key support in webhook-auth.ts; no rotation test |

### Required Before Production

- [ ] Legacy fallback path enforces date-based disabling
- [ ] Metrics counter for fallback usage (per-request, not just log)
- [ ] Alert threshold for fallback usage configured
- [ ] Key rotation procedure documented
- [ ] Cross-service HMAC golden tests passing in both repos

### Negative Test Scenarios

| # | Scenario | Expected |
|---|---|---|
| N1 | Modified payload after signing | 401 invalid signature |
| N2 | Wrong path in signing string | 401 invalid signature |
| N3 | Wrong HTTP method | 401 invalid signature |
| N4 | Expired timestamp (>5 min) | 401 expired timestamp |
| N5 | Future timestamp | 401 future timestamp |
| N6 | Missing Key-Id header | 401 missing header |
| N7 | Unknown Key-Id | 401 unknown key |
| N8 | Replayed request (same event_id) | 200 idempotent return |
| N9 | Legacy API key before cutoff | 200 (with warning) |
| N10 | Legacy API key after cutoff | 401 rejected |
| N11 | Trailing slash mismatch | 401 invalid signature |
| N12 | Query string in path | 401 query string not allowed |

---

## 4. Acknowledgment Contract

### Existing Flow

```
Sales Ops → POST handoff → SaaS Admin creates core_contact → PATCH /api/v1/leads/{leadId} (fire-and-forget callback)
```

### Required Enhancement

```
Sales Ops → POST handoff → SaaS Admin → [validate + resolve + provision]
  → POST /api/v1/webhooks/sales-ops/handoff-acknowledged { tenant_id, handoff_id, status }
  → Sales Ops updates lead to HANDED_OFF
```

The acknowledgment must be:
- [ ] Signed with HMAC-SHA256 (inverse: SaaS Admin signs, Sales Ops verifies)
- [ ] Idempotent (Sales Ops must handle duplicate acknowledgments)
- [ ] Containing `tenant_id` for cross-service traceability

---

## 5. Organization and ContactPoint Mapping

### Implementation Status

| Check | Status |
|---|---|
| Organization resolution (dedup by name + jurisdiction) | [ ] Not implemented |
| ContactPoint resolution (dedup by email + phone) | [ ] Not implemented |
| ENT-012 Organization created or linked | [ ] Not implemented |
| ENT-014 ContactPoint created or linked | [ ] Not implemented |
| Verification status preserved during handoff | [ ] Not implemented |
| Source provenance tracked (`source_customer_candidate_id`) | [ ] Not implemented |

---

## 6. Tenant-Creation Transaction

### Required Behavior

The tenant creation from handoff must be a single atomic operation:

```text
BEGIN
  1. Check idempotency (handoff_id already processed? → return existing)
  2. Resolve or create ENT-012 Organization
  3. Resolve or create ENT-014 ContactPoints
  4. Create ENT-001 Tenant
  5. Create product_entitlements for each approved product
  6. Create onboarding_cases entry
  7. Assign CSM
  8. Create provisioning_requests record
  9. Emit tenant.created event
  10. Send acknowledgment to Sales Ops
COMMIT
```

If any step fails, the entire transaction rolls back. The handoff remains retryable.

---

## 7. Audit Evidence

Every cross-service operation must produce audit events:

| Operation | Audit event | Actor |
|---|---|---|
| Handoff received | `handoff.received` | SaaS Admin |
| Organization created | `organization.created` | SaaS Admin (from Sales Ops handoff) |
| ContactPoint created | `contact.created` | SaaS Admin (from Sales Ops handoff) |
| Tenant created | `tenant.created` | SaaS Admin (from Sales Ops handoff) |
| Entitlements configured | `entitlement.created` | SaaS Admin |
| Acknowledgment sent | `handoff.acknowledged` | SaaS Admin |

All audit events must carry: `correlation_id` (from handoff), `causation_id`, `actor_type`, `actor_id`, `authority_class`, `policy_version_id`.

---

## 8. Error Taxonomy

| Error | HTTP Status | Consumer action | Retryable? |
|---|---|---|---|
| Invalid signature | 401 | Fix signing key | No (needs code fix) |
| Expired timestamp | 401 | Resend with fresh timestamp | Yes |
| Schema validation failure | 400 | Fix payload against frozen schema | No (needs code fix) |
| Duplicate handoff (same checksum) | 200 | Accept idempotent response | N/A |
| Duplicate handoff (different checksum) | 409 | Investigate — possible tampering or version mismatch | No |
| Organization conflict (fuzzy match) | 409 | Manual resolution required | No |
| SaaS Admin internal error | 500 | Retry with backoff | Yes |
| Tenant creation failed (partial) | 500 | Transaction rolled back; retry | Yes |

---

## Certification Status

**CONDITIONAL CERTIFICATION — NOT YET CERTIFIED**

The 8 passing SaaS Admin receiver smoke tests establish the basic receiver path (valid handoff → contact creation, duplicate → idempotent, missing signature → 401, existing tenant handling). They do NOT yet prove the security contract, transactional integrity, or identity resolution.

Certification requires all 28 Gate 5A tests and all 23 Gate 5C tests passing from the full 62-test matrix. Below are the mandatory test suites still required.

---

## Tests Already Passing (8/62 from the combined matrix)

| Test | Gate | What it proves |
|---|---|---|
| 5A-01 | Valid HMAC handoff reaches receiver | Basic receiver path exists |
| 5A-02 | Valid payload creates contact | Minimum payload processing works |
| 5A-03 | Missing lead_id → 400 | Required field validation works |
| 5A-04 | Idempotent replay → original result | Basic dedup at DB level |
| 5A-05 | Missing signature headers → 401 | Auth guard exists |
| 5C-03 | Existing tenant → entitlements added | Multi-product on same tenant |
| 5A-?? | New customer path creates tenant | Basic tenant creation from handoff |
| 5A-?? | Duplicate handoff returns idempotent | Idempotency key check works |

**These 8 tests prove the receiver path exists. They do NOT prove it is secure, consistent, or recoverable.**

---

## Still Required: HMAC and Replay Security (Gate 5A subset)

Beyond the basic "missing signature → 401," these negative tests must pass:

| ID | Test | Why it's more than "missing signature" |
|---|---|---|
| 5A-06 | Malformed signature rejected | Tests boundary: hex decode failure |
| 5A-07 | Incorrect signature (wrong key) rejected | Tests key isolation |
| 5A-08 | Altered payload after signing rejected | Tests body hash verification |
| 5A-09 | Wrong canonical path rejected | Tests path binding in signing string |
| 5A-10 | Wrong HTTP method rejected | Tests method binding |
| 5A-11 | Unknown key ID rejected | Tests key registry lookup |
| 5A-12 | Expired timestamp rejected | Tests replay window enforcement |
| 5A-13 | Future timestamp rejected | Tests clock skew detection |
| 5A-19 | Invalid HMAC + valid legacy API key → **still rejected** | HMAC presence blocks legacy fallback |

---

## Still Required: Idempotency Assertions (Gate 5C subset)

The current replay test checks HTTP status only. Must assert:

| ID | Assertion |
|---|---|
| 5C-14 | Same `organization_id` returned on replay |
| 5C-15 | Same `tenant_id` returned on replay |
| 5C-15a | Same entitlement IDs returned |
| 5C-15b | Same onboarding reference returned |
| 5C-15c | No additional database rows (count unchanged) |
| 5C-15d | No duplicate outbox event |
| 5C-15e | No duplicate audit mutation |
| 5C-15f | Response includes `idempotent_replay: true` |
| 5C-15g | First: 201 Created; Replay: 200 OK with original result |

---

## Still Required: Same-ID/Different-Checksum (Gate 5A)

| ID | Test |
|---|---|
| 5A-15 | Same `handoff_id` + different checksum → 409 Conflict + security audit event |
| 5A-16 | Same application + different `handoff_id` → accepted (new handoff, not a conflict) |

5A-15 must NEVER be treated as an ordinary replay. It indicates tampering or version mismatch.

---

## Still Required: Legacy API-Key Cutoff (Gate 5A subset)

| ID | Test |
|---|---|
| 5A-17 | Legacy API key before 2026-09-01 → accepted with warning log |
| 5A-18 | Legacy API key on 2026-09-01 → 410 Gone rejection |
| 5A-19 | Invalid HMAC + valid legacy key → HMAC takes precedence (still 401) |
| 5A-20 | Fallback counter increments on legacy use |
| 5A-21 | Fallback audit event created |

---

## Still Required: Identity Resolution (Gate 5C subset)

| ID | Test |
|---|---|
| 5C-01 | New organization created |
| 5C-02 | Existing org without tenant → resolved (no duplicate org) |
| 5C-03 | ✅ Already passing |
| 5C-04 | Matching email + conflicting legal identity → manual review queue |
| 5C-05 | Matching domain + conflicting org → manual review |
| 5C-06 | Duplicate ContactPoint resolved |

---

## Still Required: Transactional Integrity (Gate 5C subset)

Inject failure after each major step and verify full rollback:

| Step | Test ID | Expected |
|---|---|---|
| Organization resolution | 5C-11 | No partial state in SaaS Admin DB |
| ContactPoint resolution | 5C-11 | No orphaned contacts |
| Tenant creation | 5C-12 | No tenant without entitlements |
| Entitlement creation | 5C-11 | All rolled back |
| Onboarding creation | 5C-11 | All rolled back |
| Audit write | 5C-12 | No audit gaps |
| Outbox write | 5C-12 | No outbox event for failed transaction |

---

## Still Required: Network Response Loss (Gate 5D subset)

| ID | Test | Why critical |
|---|---|---|
| 5D-04 | SaaS Admin commits → network fails → Sales Ops retries → returns original (no duplicate) | Classic distributed-systems failure: transaction committed but acknowledgment lost |

---

## Certification Path

1. Pass all 24 still-required Gate 5A tests (contract + security)
2. Pass all 20 still-required Gate 5C tests (MDM + transactional)
3. Pass 5D-04 (network response loss)
4. Then: Phase 4 CERTIFIED
