# Gate 0R — Blocker-Resolution Directive

**Effective:** 2026-08-01
**Decision:** CONDITIONAL GO — BLOCKER REMEDIATION ONLY
**Applies to:** CTO-Knowledge-Orchestrator, Sales Ops coding agents, SaaS Admin coding agents

ALL agents must restrict work to the blocker-resolution scope below. No state migration, new features, or production rollout is authorized.

---

# 1. CTO-Knowledge-Orchestrator Instructions

The CTO-Knowledge-Orchestrator owns contract and lifecycle freeze decisions.

## A. Publish EventEnvelope v1.1.0

Do NOT alter frozen EventEnvelope v1.0.1 in place. Create v1.1.0 (minor version bump — the semantic change to nullable `tenant_id` and expanded authority classes may affect existing consumers).

### Rule

```text
tenant_id:
  field must exist
  value may be null before tenant creation
  value must be non-null for tenant-scoped events
```

### Pre-tenant event example

```json
{
  "tenant_id": null,
  "aggregate_type": "tv.salesops.Lead",
  "aggregate_id": "application_uuid",
  "sensitivity_class": "INTERNAL_CONFIDENTIAL",
  "authority_domain": "salesops",
  "authority_class": "salesops_act_bounded"
}
```

### Deliverables

- JSON Schema (v1.1.0)
- TypeScript types
- Python models
- Golden fixtures
- Positive contract tests
- Negative contract tests
- Version compatibility matrix
- Consumer migration guidance

## B. Freeze the Sales Ops Lifecycle

Review all three current state systems: TypeScript string union (`LeadFunnelStage`), TypeScript enum (`PipelineStage`), Python pipeline phases (`pipeline_phases.py:PHASES`).

### Lead Lifecycle (23 states)

```
DISCOVERED → NORMALIZED → PROFILED → CONTACT_ENRICHED
→ VALIDATION_PENDING → VERIFIED → REJECTED
→ SCORED → QA_PENDING → REMEDIATION_REQUIRED
→ OUTREACH_APPROVED → CAMPAIGN_ELIGIBLE → IN_CAMPAIGN
→ ENGAGED → UNRESPONSIVE → SUPPRESSED
→ APPLICATION_STARTED → APPLICATION_SUBMITTED
→ QUALIFICATION_REVIEW → APPROVED_CUSTOMER
→ REJECTED_CUSTOMER → HANDOFF_PENDING → HANDED_OFF
```

### Customer Application Lifecycle (10 states)

```
DRAFT → SUBMITTED → VALIDATION_PENDING → UNDER_REVIEW
→ MORE_INFORMATION_REQUIRED → APPROVED → REJECTED
→ WITHDRAWN → EXPIRED → HANDED_OFF
```

### Cross-model relationship

```
lead.APPLICATION_STARTED → creates → customer_application.DRAFT
```

### Deliverables

- `sales_lead_state_registry.yaml`
- `sales_application_state_registry.yaml`
- `sales_transition_registry.yaml`
- `sales_reason_code_registry.yaml`
- `legacy_state_mapping.yaml`

Every transition must define: source, destination, authorized actor, preconditions, required evidence, side effects, event emitted, failure reason, reversal policy.

No database migration may begin before these registries are approved.

## C. Freeze the Handoff Contract

Review `SALES_OPS_HANDOFF_CONTRACT_V1.schema.json`. Publish as `SalesOpsApprovedCustomerHandoff v1.0.0`.

Confirm it contains no legal-product entities and correctly maps through SaaS Admin to: ENT-012 Organization, ENT-014 ContactPoint, ENT-001 Tenant creation input, product entitlement configuration.

## D. Freeze Webhook Security

Define the canonical signing contract:

- HMAC-SHA256
- Caller identity: `tv-sales-ops-to-saas-admin-v1`
- Receiver identity: `TrueVow_SaaS_Administration_Service`
- HTTP method: POST
- Canonical path: `/api/v1/webhooks/sales-ops/application-approved`
- Signing string: `timestamp:method:path:bodyHash`
- Headers: `X-TrueVow-Key-Id`, `X-TrueVow-Timestamp`, `X-TrueVow-Signature`
- Replay window: 300,000 ms
- Key rotation: secondary key support via `TRUEVOW_WEBHOOK_SECONDARY_KEYS`
- Environment: per-environment keys (no cross-environment secrets)
- Legacy cutoff: 2026-09-01

Simple API-key-only authentication is NOT sufficient.

## E. Correct Architecture Records

Update `service-dependency-map.md`:
- Mark `handle_tenant_created` as LIVE per verified code
- Mark `SaaSAdminCRMClient.sync_lead()` as LIVE
- Add Sales Ops → CS-Support handoff flow
- Add App2→App3 violation note with remediation ETA

## F. Reissue Gate Decision

After remediation, produce `CTO_GATE_0_REASSESSMENT.md`. Allowed outcomes: GO, CONDITIONAL GO, NO-GO.

---

# 2. Sales Ops Coding-Agent Instructions

## A. Disable App2 → App3 Violation (B0)

Locate every path invoking `provisionTenant()` or otherwise writing/calling App3 directly.

### Requirements

- Disable the direct production path immediately
- Preserve evidence of prior behavior (do not delete, archive the call site)
- Add a failing architectural test preventing App2 → App3 calls
- Route approved-customer handoff ONLY to SaaS Admin
- Do NOT create a temporary alternate direct integration

### Files to modify

- `TrueVow_Sales_Ops_Service/lib/integrations/tenant-application-service.ts` — disable/guard `provisionTenant()`
- `TrueVow_Sales_Ops_Service/lib/services/lead-promotion-service.ts` — remove `tenantClient.provisionTenant()` call
- Add test: `__tests__/architecture/app2-app3-boundary.test.ts` — fails if any App2→App3 call path exists

Sales Ops MUST terminate at `SalesOpsApprovedCustomerHandoff`. It must NOT provision INTAKE or another tenant service.

## B. Remove Sensitive-Attribute Inference (B3)

Remove Python phases 7 and 8 from the canonical and executable production pipeline.

### Requirements

- Stop new inference and classification
- Stop segregation or campaign-routing side effects
- Remove these phases from pipeline completion criteria (`COMPLETENESS_CHECKLIST`)
- Remove dependencies from campaign eligibility
- Remove dependencies from qualification and approval
- Preserve audit history (do not delete existing records without approved retention decision)
- Isolate existing historical tables (`special_cohort_leads`, `attorney_cohort_leads`) from normal Sales Ops queries
- Add tests proving the canonical pipeline works without these phases

### Files to modify

- `scripts/pipeline_phases.py` — phases 7 and 8 already marked DEPRECATED
- `scripts/run_state_pipeline.py` — remove phases 7-8 from STEPS
- Add test: `scripts/tests/pipeline_no_sensitive_inference.py` — runs phases 1-6 only, verifies 0 sensitive classifications

### Deliverable

Produce `SENSITIVE_ATTRIBUTE_PIPELINE_REMOVAL_REPORT.md` with:
- Before/after pipeline phase count
- Affected tables
- Affected scripts (archived, not deleted)
- New default pipeline verification results
- Test evidence

## C. Do NOT Migrate States Yet (B2)

Until the CTO publishes the frozen registries:

- Do NOT rename database statuses
- Do NOT rewrite historical `pipeline_stage` records
- Do NOT remove existing `LeadFunnelStage` type or `PipelineStage` enum
- Do NOT change UI status labels
- Do NOT merge the three state systems

### Permitted preparation

- Produce read-only impact report listing every `pipeline_stage` value in the database
- Produce migration draft mapping legacy values → canonical states
- Produce dry-run SQL migration script (do not execute)

## D. Implement Canonical Event Builder (B7)

After EventEnvelope v1.1.0 freezes, all Sales Ops events must be created through ONE shared builder.

No factory, legacy agent or Python job may construct custom event dictionaries independently.

### Builder requirements

The event builder must populate ALL EventEnvelope v1.1.0 fields.

For pre-tenant events: `tenant_id = null`

Must validate: event type, event version, aggregate, authority, policy, sensitivity, correlation, causation, timestamp, producer identity.

Must emit: conformant JSON matching the frozen JSON Schema.

### Files to create

- `TrueVow_Sales_Ops_Service/lib/events/event-builder.ts` — TypeScript canonical event builder
- `TrueVow_Sales_Ops_Service/scripts/events/event_builder.py` — Python canonical event builder
- `__tests__/events/event-builder.test.ts` — TypeScript tests against golden fixtures
- `scripts/tests/event_builder_test.py` — Python tests against golden fixtures

## E. Upgrade Webhook Sending (B4)

Replace API-key-only requests with the frozen HMAC-SHA256 signing contract.

### Requirements

- Signature header: `X-TrueVow-Signature`
- Key ID: `X-TrueVow-Key-Id: tv-sales-ops-to-saas-admin-v1`
- Timestamp: `X-TrueVow-Timestamp` (milliseconds)
- Payload digest: SHA-256 of raw body bytes
- Replay-safe idempotency key via `event_id`
- Correlation ID for traceability
- Handoff ID for deduplication

Keep the API key ONLY if the final security contract explicitly retains it as an additional layer. The HMAC MUST be present and verified.

### Files to modify

- `TrueVow_Sales_Ops_Service/lib/integrations/saas-admin/webhook-client.ts`
- Add test: `__tests__/security/webhook-signature.test.ts` — TypeScript golden fixture tests

---

# 3. SaaS Admin Coding-Agent Instructions

## A. Remove Reliance on Direct Sales Ops Provisioning

Confirm SaaS Admin is the ONLY permitted bridge from App2 into tenant creation and App3 provisioning.

Reject attempts by Sales Ops to invoke App3 provisioning directly.

### Requirements

- Add architecture test proving Sales Ops can call SaaS Admin handoff endpoint
- Add architecture test proving Sales Ops CANNOT call INTAKE provisioning
- Add architecture test proving SaaS Admin owns downstream provisioning initiation

### Files to create

- `TrueVow_SaaS_Administration_Service/tests/architecture/trust-boundary.test.ts`

## B. Upgrade Webhook Verification (B4)

Implement the frozen HMAC-SHA256 verification contract for `POST /webhooks/sales-ops/application-approved`.

Verification MUST occur BEFORE: payload parsing into domain objects, Organization mutation, ContactPoint mutation, Tenant creation, Entitlement creation, audit-side business processing.

### Test scenarios

- Invalid signature → rejected
- Wrong path → rejected
- Wrong method → rejected
- Wrong environment → rejected
- Expired timestamp → rejected
- Replayed request (same event_id) → rejected or idempotent return
- Unknown key ID → rejected
- Modified payload → rejected
- Duplicate valid handoff → idempotent return

### Files to modify

- `TrueVow_SaaS_Administration_Service/app/api/v1/webhooks/sales-ops/application-approved/route.ts`
- Add test: `tests/security/sales-ops-webhook-signature.test.ts`

## C. Confirm Live tenant.created Implementation (B5)

The audit found `handle_tenant_created` is live despite stale documentation.

### Requirements

Produce code-backed evidence covering: exact entry point, caller, receiver, request schema, signature validation, idempotency, database mutations, downstream call, failure behavior, tests, production wiring.

Do NOT merely relabel it LIVE because a function exists. Confirm the full path is executable and tested.

### Deliverable

`docs/gate-0-audit/TENANT_CREATED_LIVE_CONFIRMATION.md`

## D. Implement Only Against Frozen Contracts

Do NOT build the new handoff consumer against draft schemas until the CTO freezes:
- EventEnvelope v1.1.0
- SalesOpsApprovedCustomerHandoff v1.0.0
- HMAC WebhookSignature contract for the Sales Ops → SaaS Admin relationship

---

# 4. Required Blocker Acceptance Tests

Gate 0R cannot be cleared until these pass:

| # | Test | Blocker |
|---|---|---|
| 1 | Pre-tenant Sales Ops event validates with `tenant_id: null` | B1 |
| 2 | Tenant-scoped event fails when `tenant_id` is null | B1 |
| 3 | All 18 canonical envelope fields are represented | B1, B7 |
| 4 | TypeScript and Python generate equivalent envelopes | B7 |
| 5 | Every current state maps to a frozen canonical state or explicit unmapped exception | B2 |
| 6 | Invalid state transitions fail closed | B2 |
| 7 | App2 cannot invoke App3 provisioning | B0 |
| 8 | Sales Ops approved-customer handoff reaches SaaS Admin | B0, B6 |
| 9 | Invalid webhook signatures are rejected | B4 |
| 10 | Replayed signed requests are rejected or return original idempotent result | B4 |
| 11 | Sensitive-attribute phases do not execute | B3 |
| 12 | Campaign eligibility does not depend on removed sensitive classifications | B3 |
| 13 | SaaS Admin resolves duplicate handoffs without duplicate tenants | B6 |
| 14 | Architecture documentation matches verified implementation | B5 |
| 15 | All previously defined forty-three commissioning tests are rerun | All |

### Gate Threshold

Required for Gate 0R to clear:
- 100% of critical tests (B0-B3)
- 100% of security-boundary tests
- 100% of contract tests
- 100% of state-transition tests for implemented scope
- No unresolved critical or high-severity blocker

The next milestone: **Gate 0R — Contract, Boundary and Compliance Remediation**
