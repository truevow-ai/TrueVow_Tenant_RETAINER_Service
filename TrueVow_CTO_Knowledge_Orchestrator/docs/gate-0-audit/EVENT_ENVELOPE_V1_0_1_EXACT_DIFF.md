# EventEnvelope v1.0.1 — Exact Schema Diff

**Audit date:** 2026-08-01
**Schema version:** EventEnvelope v1.0.1 (frozen)
**Sources:** RETAINER `event-envelope.schema.json`, RETAINER `openapi.yaml`, SaaS Admin migration 173 golden fixture, SaaS Admin `lib/contracts/index.ts`

---

## Exact 18-Field Definition (Canonical)

| # | Field | Type | Constraints | Required |
|---|---|---|---|---|
| 1 | `event_id` | `string` (uuid) | RFC 9562 | YES |
| 2 | `event_type` | `string` | regex `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$` | YES |
| 3 | `occurred_at` | `string` (ISO 8601) | `format: date-time` | YES |
| 4 | `recorded_at` | `string` (ISO 8601) | `format: date-time` | YES |
| 5 | `tenant_id` | `string` (uuid) | Non-null | YES |
| 6 | `aggregate_type` | `string` | `minLength: 1` | YES |
| 7 | `aggregate_id` | `string` (uuid) | — | YES |
| 8 | `aggregate_version` | `integer` | `minimum: 1` | YES |
| 9 | `actor_type` | `string` | `minLength: 1` | YES |
| 10 | `actor_id` | `string` (uuid or `minLength: 1`) | oneOf | YES |
| 11 | `authority_class` | `string` (enum) | SYS_ADMIN, FIRM_POLICY, STAFF_AUTH, ATTY_AUTH, CLIENT_AUTH, PROHIBITED | YES |
| 12 | `authority_record_id` | `string` (uuid or null) | oneOf | YES |
| 13 | `policy_version_id` | `string` (uuid or null) | oneOf | YES |
| 14 | `correlation_id` | `string` (uuid) | — | YES |
| 15 | `causation_id` | `string` (uuid or null) | oneOf | YES |
| 16 | `payload` | `object` | Schema-validated minimal payload | YES |
| 17 | `sensitivity_class` | `string` | `minLength: 1` | YES |
| 18 | `schema_version` | `string` | regex `^[0-9]+\.[0-9]+\.[0-9]+$` | YES |

---

## Comparison Against Sales Ops Event Structures

### A. `ApprovedApplicationPayload` (application-approved webhook)

**File:** `TrueVow_Sales_Ops_Service/lib/integrations/saas-admin/webhook-client.ts`
**Type:** Inline in `sendApprovedApplication()` body

| Canonical field | Sales Ops equivalent | Compatibility | Migration required |
|---|---|---|---|
| `event_id` | ❌ None (uses `X-Request-ID` header) | FAIL | Add UUID event_id |
| `event_type` | ❌ None (implicit: `sales.application.approved`) | FAIL | Add event_type |
| `occurred_at` | `application_timestamp` (string) | PARTIAL — not ISO 8601 guaranteed | Standardize to ISO 8601 |
| `recorded_at` | ❌ None | FAIL | Add recorded_at |
| `tenant_id` | ❌ None | N/A (pre-tenant) | Set to `null` |
| `aggregate_type` | ❌ None | FAIL | Add `tv.salesops.CustomerApplication` |
| `aggregate_id` | `lead_id` | PARTIAL — needs namespace | Map to aggregate_id |
| `aggregate_version` | ❌ None | FAIL | Track version or set to 1 |
| `actor_type` | ❌ None | FAIL | Add `system` or `human` |
| `actor_id` | ❌ None | FAIL | Add Sales Ops agent identity |
| `authority_class` | ❌ None | FAIL | Add `APPROVE` (Sales Ops class) |
| `authority_record_id` | ❌ None | FAIL | Add approval record reference |
| `policy_version_id` | ❌ None | FAIL | Add canopy ontology version |
| `correlation_id` | ❌ None (X-Request-ID is similar) | FAIL | Add correlation_id |
| `causation_id` | ❌ None | FAIL | Add prior event reference |
| `payload` | All 10 data fields (lead_id, firm_name, etc.) | PARTIAL — informal, not schema-validated | Wrap in `payload` object |
| `sensitivity_class` | ❌ None | FAIL | Add `INTERNAL_CONFIDENTIAL` |
| `schema_version` | ❌ None | FAIL | Add `1.0.1` |

**Result: 0/18 fields fully compatible. 3/18 partial. 15/18 missing.**

### B. `createTenant()` payload (POST /api/v1/tenants)

**File:** `TrueVow_Sales_Ops_Service/lib/integrations/platform-service.ts:75`
**Body:** `{ firm_name, contact_email, subscription_plan, lead_id }`

| Status | Fields present |
|---|---|
| **Not an event** — this is a command/provisioning call, not an event emission | firm_name, contact_email, subscription_plan, lead_id |
| Should be wrapped in EventEnvelope or at minimum carry correlation_id + causation_id | No envelope fields |

### C. `createCustomerHandoff()` payload (POST /api/v1/customer-handoffs)

**File:** `TrueVow_Sales_Ops_Service/lib/integrations/cs-support-service.ts:125`
**Body:** `{ tenant_id, lead_id, handoff_reason, contact_name, contact_email, contact_phone }`

| Status | Fields present |
|---|---|
| Operationally closer to an event but uses CS-Support's format | tenant_id present (after provisioning), handoff_reason |

---

## Key Gaps

### 1. `tenant_id` is non-nullable in frozen EventEnvelope v1.0.1

**Problem:** Sales Ops events occur before SaaS Admin creates a Tenant. Setting `tenant_id` to a dummy UUID violates the semantics — but `null` violates the frozen schema constraint `"type": "uuid"` with no `nullable: true`.

**Resolution required:** Either:
- A. Accept that `tenant_id` is `null` for pre-tenant Sales Ops events (requires contract amendment)
- B. Use a sentinel `tenant_id` before tenant creation (risks leaking pre-tenant data into tenant scopes)
- C. Define a `SalesOpsEventEnvelope` that extends EventEnvelope with `tenant_id` nullable

**Recommendation:** Option A with explicit contract consultation. The frozen contract was designed for the legal-product domain where `tenant_id` is always known. Sales Ops events are a new consumer.

### 2. `authority_class` uses legal-product enums, not Sales Ops enums

**Problem:** The frozen `authority_class` enum has 6 values (SYS_ADMIN, FIRM_POLICY, STAFF_AUTH, ATTY_AUTH, CLIENT_AUTH, PROHIBITED) designed for legal-product authority. Sales Ops uses 7 different classes (OBSERVE, RECOMMEND, DRAFT, ACT_BOUNDED, APPROVE, ADMINISTER, NEVER_AUTOMATE).

**Resolution required:** Either:
- A. Extend the frozen enum with Sales Ops values (contract amendment)
- B. Map Sales Ops classes to closest legal class (APPROVE → FIRM_POLICY) — lossy
- C. Add `authority_domain` field to disambiguate

**Recommendation:** Option A — contract amendment to add `salesops:*` authority classes.

### 3. `aggregate_type` uses ENT-XXX entity identifiers

**Problem:** The canonical `aggregate_type` field expects values like `ENT-041` (Matter). Sales Ops aggregates would need `tv.salesops.*` namespace identifiers.

**Resolution:** Define Sales Ops aggregate types: `tv.salesops.Lead`, `tv.salesops.CustomerApplication`, `tv.salesops.HandoffPackage`, etc.

---

## Defaulting Rules for Sales Ops Events

For pre-tenant Sales Ops events emitted before SaaS Admin handoff:

| Field | Default value | Rationale |
|---|---|---|
| `tenant_id` | `null` (requires contract amendment) | No tenant exists yet |
| `sensitivity_class` | `INTERNAL_CONFIDENTIAL` | Sales Ops data is internal |
| `authority_class` | `ACT_BOUNDED` or `APPROVE` (requires enum extension) | Sales Ops operational authority |
| `authority_record_id` | Derived from approval decision reference | Traceable to commercial approval |
| `policy_version_id` | UUID of `sales-ops-ontology-v1.0.0` | Version-lock at execution |
| `schema_version` | `1.0.1` | Same envelope version |
| `recorded_at` | Set to `occurred_at` if not available | Same instant if emitted synchronously |
| `causation_id` | `null` for origin events | No prior event for discovery events |
