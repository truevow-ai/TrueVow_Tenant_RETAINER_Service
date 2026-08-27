# CTO Gate 0 Decision — Revised (Gate 0R)

**Decision date:** 2026-08-01
**Decision authority:** CTO-Knowledge-Orchestrator (Yasha)
**Status:** CONDITIONAL GO — BLOCKER REMEDIATION ONLY

---

## Decision

**CONDITIONAL GO — GATE 0R REMEDIATION ONLY**

**Actual status:** 1 blocker closed (B5), 3 partially remediated (B1, B2, B3), 4 not yet implemented (B0, B4, B6, B7).

This decision does NOT authorize:
- Sales Ops state migration
- New Sales Ops features
- Broader SaaS Admin onboarding work
- Tenant activation work
- New App3 provisioning behavior
- Changes to the legal-product ontology
- Production rollout

Authorized work is restricted to the blocker-resolution scope below. Branch structure per CTO directive: `cto/gate0-*`, `salesops/gate0-*`, `saasadmin/gate0-*`.

---

## Revised Blocker Register — Current Status

| ID | Severity | Blocker | Status | Owner | Required result |
|---|---|---|---|---|---|
| **B0** | **CRITICAL** | App2 directly provisions App3 | **Open** | Sales Ops | Remove direct path; all provisioning through SaaS Admin |
| **B1** | **CRITICAL** | EventEnvelope cannot represent pre-tenant events | **Partial** | CTO + Sales Ops + SaaS Admin | Publish v1.1.0 with nullable tenant_id (JSON Schema + TS done; Python + fixtures + matrix pending) |
| **B2** | **CRITICAL** | No canonical Sales Ops lifecycle | **Partial** | CTO + Sales Ops | Freeze registries (ontology YAML done; transition/reason-code/legacy mapping pending) |
| **B3** | **CRITICAL** | Sensitive-attribute inference in production | **Partial** | Sales Ops | Remove from execution (pipeline_phases.py deprecated done; runner + test + report pending) |
| **B4** | **HIGH** | Webhook uses simple API key | **Open** | CTO + Sales Ops + SaaS Admin | HMAC-SHA256 sender + receiver + key registry + golden tests |
| **B5** | **HIGH** | Stale dependency documentation | **Closed** | CTO | `service-dependency-map.md` corrected |
| **B6** | **HIGH** | No frozen handoff contract | **Open** | CTO | Review, approve, freeze `SalesOpsApprovedCustomerHandoff v1.0.0` |
| **B7** | **HIGH** | 0/18 envelope conformity | **Open** | Sales Ops | Central event builder emits conformant envelopes |

---

## Blocker Details

### B0 — App2 Directly Provisions App3 (CRITICAL)

**Files:** `TrueVow_Sales_Ops_Service/lib/integrations/tenant-application-service.ts:232`
**Code:** `POST /api/v1/tenants/provision` (Sales Ops → INTAKE Service)

Sales Ops (App2, MEDIUM trust) calls INTAKE tenant provisioning endpoint (App3, EXTERNAL) directly. This violates the platform trust boundary and bypasses SaaS Admin. Tenant provisioning must only be triggered by SaaS Admin after receiving the handoff package from Sales Ops.

**Required result:** Remove or bypass-disable the direct path. Route approved-customer handoff only to SaaS Admin. Add failing architectural test preventing App2 → App3 calls.

### B1 — EventEnvelope Cannot Represent Pre-Tenant Events (CRITICAL)

**Files:** `event-envelope.schema.json`, `lib/contracts/index.ts`

The frozen `EventEnvelope v1.0.1` requires non-null `tenant_id` and uses legal-product-only authority classes. Sales Ops events occur before tenant creation and use operational authority classes. Do NOT silently edit v1.0.1. Create v1.1.0 (minor version bump — the semantic change to nullable `tenant_id` and expanded authority may affect existing consumers).

**Rule:** `tenant_id` field must exist. Value may be null before tenant creation. Value must be non-null for tenant-scoped events.

### B2 — No Canonical Sales Ops Lifecycle (CRITICAL)

Three competing state systems exist in one codebase with no canonical source of truth. No database migration may begin before the state and transition registries are approved and frozen.

### B3 — Sensitive-Attribute Inference in Production Pipeline (CRITICAL)

Python Phases 7-8 (`cohort_firm_tag.py`, `cohort_firm_segregate.py`, `cohort_attorney_segregate.py`) infer community affiliation from names using `name_ethnicity_lookup.json` (5000+ entries). Must stop production execution and run only with explicit human authorization under defensible criteria.

### B4 — Simple API Key Instead of HMAC (HIGH)

`SaaSAdminWebhookClient.sendApprovedApplication()` uses plain `X-API-Key` string comparison. The frozen `WebhookSignature v1.0` contract requires HMAC-SHA256 with `X-TrueVow-Key-Id`, `X-TrueVow-Timestamp`, `X-TrueVow-Signature` headers. Legacy bearer auth cutoff is 2026-09-01.

### B5 — Stale Documentation (HIGH)

`service-dependency-map.md` marks `handle_tenant_created` as TODO stub. Verified code shows it is LIVE in `onboarding-orchestrator.ts:78-118`. Must correct platform map and dependency status from verified code.

### B6 — No Frozen Handoff Contract (HIGH)

No `SalesOpsApprovedCustomerHandoff` schema exists. The generated candidate schema at `SALES_OPS_HANDOFF_CONTRACT_V1.schema.json` must be reviewed, approved, and versioned.

### B7 — 0/18 Event Envelope Conformance (HIGH)

No Sales Ops event populates EventEnvelope fields. A central event builder must be implemented that emits fully conformant envelopes, with `tenant_id: null` for pre-tenant events.

---

## Immediate Execution Order

```
1.  B0 — Disable direct App2 → App3 provisioning path
2.  B3 — Remove sensitive-attribute phases from production execution
3.  B1 — Freeze EventEnvelope v1.1.0
4.  B2 — Freeze Sales Ops lifecycle and transition registries
5.  B6 — Freeze SalesOpsApprovedCustomerHandoff v1.0.0
6.  B4 — Replace API-key-only webhook auth with HMAC-SHA256
7.  B5 — Correct verified architecture documentation
8.  B7 — Implement the canonical Sales Ops event builder
9.  (Gate 0R reassessment)
10. State migrations (after GO decision)
11. Re-run all 43 Gate 0 commissioning tests
```

---

## Gate Threshold

Gate 0R must not move to GO merely because more than half the tests pass.

Required:
- 100% of critical tests (B0-B3)
- 100% of security-boundary tests
- 100% of contract tests
- 100% of state-transition tests for implemented scope
- No unresolved critical or high-severity blocker

The next milestone is:

> **Gate 0R — Contract, Boundary and Compliance Remediation**

The success condition is not merely increasing the current 4/43 result. It is closing every critical and high-severity blocker, then rerunning the entire commissioning matrix under the frozen contracts.

---

## Canonical Lifecycle Freeze

Do not migrate any state yet. First freeze two separate Sales Ops state models.

### Lead lifecycle (23 states)

```
DISCOVERED → NORMALIZED → PROFILED → CONTACT_ENRICHED
→ VALIDATION_PENDING → VERIFIED → SCORED
→ QA_PENDING → OUTREACH_APPROVED → CAMPAIGN_ELIGIBLE
→ IN_CAMPAIGN → ENGAGED → APPLICATION_STARTED
→ APPLICATION_SUBMITTED → QUALIFICATION_REVIEW
→ APPROVED_CUSTOMER → HANDOFF_PENDING → HANDED_OFF

Branches: REJECTED | SUPPRESSED | REMEDIATION_REQUIRED | UNRESPONSIVE | FAILED
```

### Customer application lifecycle (10 states)

```
DRAFT → SUBMITTED → VALIDATION_PENDING → UNDER_REVIEW
→ MORE_INFORMATION_REQUIRED → APPROVED → REJECTED
→ WITHDRAWN → EXPIRED → HANDED_OFF
```

### Cross-model relationship

```
lead.APPLICATION_STARTED → creates → customer_application.DRAFT
```

Do not force lead, application, campaign, approval and handoff statuses into one database column.

---

## EventEnvelope v1.1.0 Pre-Tenant Example

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440001",
  "event_type": "salesops.lead.discovered",
  "occurred_at": "2026-08-01T00:00:00Z",
  "recorded_at": "2026-08-01T00:00:00Z",
  "tenant_id": null,
  "aggregate_type": "tv.salesops.Lead",
  "aggregate_id": "uuid",
  "aggregate_version": 1,
  "actor_type": "system",
  "actor_id": "salesops.pipeline.scraper",
  "authority_domain": "salesops",
  "authority_class": "salesops_act_bounded",
  "authority_record_id": "uuid",
  "policy_version_id": "uuid",
  "correlation_id": "uuid",
  "causation_id": null,
  "payload": {"firm_name": "Smith Law Firm", "source": "google_maps"},
  "sensitivity_class": "INTERNAL_CONFIDENTIAL",
  "schema_version": "1.0"
}
```

---

## Blocker Acceptance Tests

Gate 0R cannot be cleared until these tests pass:

1. Pre-tenant Sales Ops event validates with `tenant_id: null`
2. Tenant-scoped event fails when `tenant_id` is null
3. All eighteen canonical envelope fields are represented
4. TypeScript and Python generate equivalent envelopes
5. Every current state maps to a frozen canonical state or an explicit unmapped exception
6. Invalid state transitions fail closed
7. App2 cannot invoke App3 provisioning
8. Sales Ops approved-customer handoff reaches SaaS Admin
9. Invalid webhook signatures are rejected
10. Replayed signed requests are rejected or return original idempotent result
11. Sensitive-attribute phases do not execute
12. Campaign eligibility does not depend on removed sensitive classifications
13. SaaS Admin resolves duplicate handoffs without duplicate tenants
14. Architecture documentation matches verified implementation
15. All previously defined forty-three commissioning tests are rerun
