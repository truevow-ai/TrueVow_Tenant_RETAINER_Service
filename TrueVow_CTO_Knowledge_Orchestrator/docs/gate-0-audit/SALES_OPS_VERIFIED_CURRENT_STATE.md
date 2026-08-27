# Sales Ops Verified Current State — Gate 0 Audit

**Audit date:** 2026-08-01
**Auditor:** CTO-Knowledge-Orchestrator (read-only)
**Repositories inspected:** `TrueVow_Sales_Ops_Service`, `TrueVow_SaaS_Administration_Service`, `TrueVow_Tenant_RETAINER_Service` (contracts), `Cross-Service/` (docs)

---

## 1. Service and Endpoint Reality

### 1.1 Webhook: `POST /webhooks/sales-ops/application-approved`

| Property | Value |
|---|---|
| **Exists?** | ✅ YES — in SaaS Admin, not Sales Ops |
| **File** | `TrueVow_SaaS_Administration_Service/app/api/v1/webhooks/sales-ops/application-approved/route.ts` (151 lines) |
| **Status** | **LIVE** — fully implemented, not a stub |
| **Called by?** | Sales Ops `SaaSAdminWebhookClient.sendApprovedApplication()` via `fetch()` |
| **Caller file** | `TrueVow_Sales_Ops_Service/lib/integrations/saas-admin/webhook-client.ts:49-67` |
| **Auth** | Simple `X-API-Key` string comparison (NOT HMAC-SHA256) |
| **What it does** | Receives application payload → creates `core_contacts` row → fires callback to Sales Ops (`updateLeadContact`) |
| **Idempotency** | Checks `core_contacts.source_lead_id` against `lead_id` (UNIQUE constraint) |
| **Error response** | Returns `200` with contact on duplicate; `500` on Supabase error |
| **Acknowledgment** | Returns `{ contact_id, lead_id, status: 'created' | 'already_exists' }` |

### 1.2 Webhook: `POST /webhooks/saas-admin` (`tenant.created`)

| Property | Value |
|---|---|
| **Exists?** | ✅ YES — in onboarding-orchestrator.ts |
| **File** | `TrueVow_SaaS_Administration_Service/lib/services/onboarding-orchestrator.ts:78-118` |
| **Status** | **LIVE** — sends HMAC-signed POST to INTAKE service |
| **Target** | `{INTAKE_SERVICE_URL}/webhooks/saas-admin` |
| **Auth** | HMAC-SHA256 via `signBody()` with `SAAS_ADMIN_WEBHOOK_SECRET` |
| **Called from** | `orchestrateOnboarding()` line 357 |
| **STUB?** | **NO** — the `service-dependency-map.md` note about `handle_tenant_created` being TODO is **STALE**. This is now implemented. |

### 1.3 All Cross-Domain Calls (Sales Ops → Other Services)

| Caller | Target | Method | Endpoint | Auth | Status |
|---|---|---|---|---|---|
| Sales Ops | SaaS Admin | `fetch()` | `POST /api/v1/webhooks/sales-ops/application-approved` | X-API-Key | LIVE |
| Sales Ops | SaaS Admin | `axios` | `POST /api/v1/tenants` | X-API-Key | LIVE |
| Sales Ops | SaaS Admin | `axios` | `POST /api/v1/provisioning/trigger` | X-API-Key | LIVE |
| Sales Ops | Tenant App | `axios` | `POST /api/v1/tenants/provision` | X-API-Key | LIVE |
| Sales Ops | CS-Support | `axios` | `POST /api/v1/customer-handoffs` | X-API-Key | LIVE |
| Sales Ops | Internal Ops | `axios` | `POST /api/v1/revops/activities` | X-API-Key | LIVE |
| Sales Ops | KYC Service | `axios` | `POST /api/v1/applications/submit` | X-API-Key | LIVE |

### 1.4 Status Classification

| Item | Status |
|---|---|
| `POST /webhooks/sales-ops/application-approved` (SaaS Admin side) | **LIVE** |
| `SaaSAdminWebhookClient.sendApprovedApplication()` (Sales Ops side) | **LIVE** |
| `tenant.created` → INTAKE (`provisionTenantApp`) | **LIVE** |
| `tenant.created` → CS-Support + Sales CRM (`tenants/route.ts`) | **LIVE** |
| `POST /api/v1/tenants` (Sales Ops → SaaS Admin for tenant creation) | **LIVE** |
| `POST /api/v1/tenants/provision` (Sales Ops → Tenant App provisioning) | **LIVE** |
| `POST /api/v1/customer-handoffs` (Sales Ops → CS-Support) | **LIVE** |
| `service-dependency-map.md` "handle_tenant_created is TODO" | **STALE DOCUMENTATION** |
| `service-dependency-map.md` "SaaSAdminCRMClient.sync_lead() — fully built, zero callers" | **LIVE** (called from application-approved route) |
| Handoff contract JSON schema | **NOT FOUND** |
| Sales Ops event envelope schema | **NOT FOUND** |
| Sales Ops HandoffPackage type definition | **NOT FOUND** |

---

## 2. EventEnvelope Schema Diff (Summary)

### 2.1 Frozen EventEnvelope v1.0.1 (18 fields)

Defined in 4 sources that agree:
- `TrueVow_Tenant_RETAINER_Service/.../contracts/event-envelope.schema.json` (JSON Schema)
- `TrueVow_Tenant_RETAINER_Service/.../contracts/openapi.yaml` (OpenAPI 3.1.0)
- `TrueVow_SaaS_Administration_Service/supabase/migrations/173_final_contract_fixes.sql` (golden fixture)
- `TrueVow_SaaS_Administration_Service/lib/contracts/index.ts` (TypeScript interface)

### 2.2 Sales Ops Actual Event Structure

Sales Ops has **no canonical event envelope definition**. What exists:

1. **`SaaSAdminWebhookClient.sendApprovedApplication()`** sends:
   ```typescript
   {
     lead_id, firm_name, contact_name, contact_email, contact_phone,
     geography_state, practice_areas, enrichment_angles, cohort_tier,
     application_timestamp
   }
   ```
   Fields not present: event_id, event_type, occurred_at, tenant_id, aggregate_type, aggregate_id, aggregate_version, actor_type, authority_class, authority_record_id, policy_version_id, correlation_id, causation_id, sensitivity_class.

2. **`PlatformServiceClient.createTenant()`** sends to `POST /api/v1/tenants`:
   ```typescript
   { firm_name, contact_email, subscription_plan, lead_id }
   ```

3. **`CSSupportServiceClient.createCustomerHandoff()`** sends to `POST /api/v1/customer-handoffs`:
   ```typescript
   { tenant_id, lead_id, handoff_reason, contact_name, contact_email, contact_phone }
   ```

None of these conform to EventEnvelope v1.0.1. Full diff in `EVENT_ENVELOPE_V1_0_1_EXACT_DIFF.md`.

---

## 3. Sales Ops Lifecycle State Audit

### 3.1 Three Competing State Systems

| System | Location | States | Status |
|---|---|---|---|
| `LeadFunnelStage` (TypeScript type) | `lib/db/repositories/leads-repository.ts:11-38` | 21 string values (7 canonical + 7 legacy + 7 post-sale) | **ACTIVE** — used by leads API, DB writes |
| `PipelineStage` (TypeScript enum) | `lib/lead-factory/types.ts:11-43` | 16 enum values (pre-processing, enrichment, HITL, errors) | **ACTIVE** — used by lead factory state machine |
| Python 8-phase pipeline | `scripts/pipeline_phases.py:32-178` | 8 phases (scraping, firmographics, attorney extraction, contacts, enrichment, browser recovery, firm cohort, attorney cohort) | **ACTIVE** — used by batch processing |

### 3.2 Legacy CRM Stages (Archived)

Found in `scripts/archive/pipeline_e2e.py`: `scraped`, `enriched`, `outreach_started`, `engaged`, `qualified`, `demo_done`, `application_submitted`, `new`, `contacted`, `discovery`, `demo_booked`, `negotiation`, `kyc_pending`, `kyc_approved`, `application_approved`, `provisioning`, `won`, `converted`, `lost`, `disqualified`, `rejected`, `waitlist`, `customer`.

### 3.3 Comparison Against Canonical Sales Ops Lifecycle

| Canonical state | In `LeadFunnelStage`? | In `PipelineStage` enum? | In Python? | DB constraint? |
|---|---|---|---|---|
| DISCOVERED | ❌ (`discovery` exists) | ❌ | ❌ (legacy `discovery`) | ❌ no enum constraint |
| NORMALIZED | ❌ | `IDENTITY_NORMALIZED` ✅ | ❌ | ❌ |
| PROFILED | ❌ | `WEBSITE_PROFILED` ✅ | ✅ (phase 2) | ❌ |
| CONTACT_ENRICHED | ❌ | `CONTACT_ENRICHED` ✅ | ✅ (phase 4) | ❌ |
| VALIDATION_PENDING | ❌ | ❌ | ❌ | ❌ |
| VERIFIED | ❌ | ❌ | ❌ | ❌ |
| SCORED | ❌ | `SIGNAL_SCORED` ✅ | ❌ | ❌ |
| QA_PENDING | ❌ | `QA_AUDITED` ✅ | ❌ | ❌ |
| OUTREACH_APPROVED | ❌ | ❌ | ❌ | ❌ |
| CAMPAIGN_ELIGIBLE | ❌ | `CAMPAIGN_READY` ✅ | ❌ | ❌ |
| IN_CAMPAIGN | ❌ | ❌ | ❌ | ❌ |
| ENGAGED | `engaged` ✅ | ❌ | ❌ | ❌ no enum constraint |
| APPLICATION_STARTED | ❌ | ❌ | ❌ | ❌ |
| APPLICATION_SUBMITTED | `application_submitted` ✅ | ❌ | ❌ | ❌ no enum constraint |
| QUALIFICATION_REVIEW | ❌ | ❌ | ❌ | ❌ |
| APPROVED_CUSTOMER | `application_approved` ✅ | ❌ | ❌ | ❌ no enum constraint |
| HANDOFF_PENDING | ❌ | ❌ | ❌ | ❌ |
| HANDED_OFF | `converted` ✅ | ❌ | ❌ | ❌ no enum constraint |

**Conclusion:** Zero canonical states are implemented. All 18 canonical states are missing. 4 canonical states have approximate equivalents in `LeadFunnelStage` (engaged, application_submitted, application_approved, converted). 6 canonical states have approximate equivalents in `PipelineStage` enum (IDENTITY_NORMALIZED, WEBSITE_PROFILED, CONTACT_ENRICHED, SIGNAL_SCORED, QA_AUDITED, CAMPAIGN_READY). No state has a DB CHECK or ENUM constraint.

---

## 4. Pipeline Audit

### 4.1 TypeScript Runtime Pipeline (lead-factory)

**16 stages** in `PipelineStage` enum (`lib/lead-factory/types.ts`):
```
MARKET_PLANNED → SCOUTED → IDENTITY_NORMALIZED → WEBSITE_PROFILED
→ CONTACT_ENRICHED → ENRICHED_DEEP → CONTACT_VALIDATED
→ SIGNAL_SCORED → QUALITY_GATED → QA_AUDITED
→ OUTREACH_ANGLE_GENERATED → INGESTED → CAMPAIGN_READY
+ HITL: PENDING_SANIA_REVIEW → SANIA_APPROVED | SANIA_REJECTED
+ Error: FAILED → QUARANTINED
```

**Idempotency:** Transition validation via `PipelineStateManager.validateTransition()` (line 75-205)
**Retry:** FAILED → SCOUTED (retry path)
**Resume:** Not implemented — no checkpointing
**Test coverage:** None found in `__tests__/` for `PipelineStateManager`

### 4.2 Python Batch Pipeline (scripts/)

**8 phases** in `pipeline_phases.py:PHASES`:
```
1. Lead Search & Scraping
2. Law Firm Information Gathering
3. Attorney Extraction
4. Contact Discovery (Emails + Phones)
5. DeepSeek Primary Enrichment
6. Gemini Flash Secondary Enrichment + Headless-Browser Recovery
7. Firm-Level Cohort Segregation
8. Attorney-Level Cohort Segregation
```

**Idempotency:** Checkpoint-based (JSON progress files), not DB idempotency keys
**Retry:** Manual restart from checkpoint
**Resume:** JSON checkpoint files (`enrich_backfill_progress.json`, etc.)
**Test coverage:** `scripts/tests/handoff_db_tests.py` (1 file), no pipeline stage unit tests

### 4.3 No Shared Pipeline Definition

The TypeScript and Python pipelines share **zero code, zero config, zero registry**. They are completely independent implementations with different stage names, different state models, and different idempotency strategies.

---

## 5. Trust-Domain Security Findings

### 5.1 Trust-Domain Architecture

| Domain | Clerk App | Trust | Services |
|---|---|---|---|
| PLATFORM_OPERATORS | App 1 | HIGH | SaaS Admin (3001), Internal Ops, CSM Core, Billing |
| SALES_SUPPORT | App 2 | MEDIUM (LLM zone) | Sales Ops (3056) |
| TENANTS | App 3 | EXTERNAL | INTAKE (3022), Customer Portal, TRACE, SETTLE |

### 5.2 Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F5-1 | **HIGH** | **App2 writing to App3 directly**: Sales Ops `TenantApplicationServiceClient.provisionTenant()` calls `POST /api/v1/tenants/provision` on INTAKE service (App3) | `lib/integrations/tenant-application-service.ts:232` |
| F5-2 | **HIGH** | **App2 writing to App3 directly**: Sales Ops `KYCServiceClient` calls `POST /api/v1/applications/submit` on an external service | `lib/integrations/kyc-service.ts:78` |
| F5-3 | **MEDIUM** | **Simple API key auth instead of HMAC**: `SaaSAdminWebhookClient` uses plain `X-API-Key` string compare, not HMAC-SHA256 | `lib/integrations/saas-admin/webhook-client.ts:49` |
| F5-4 | **MEDIUM** | **No idempotency key on handoff**: `sendApprovedApplication()` uses `X-Request-ID` header but the receiver checks `source_lead_id` uniqueness, not an idempotency key | `webhook-client.ts:63` |
| F5-5 | **LOW** | **Sensitive attribute inference in production**: `cohort_firm_tag.py`, `cohort_attorney_segregate.py` infer community/ethnicity from names using `name_ethnicity_lookup.json` (5000+ entries) | `scripts/cohort_firm_tag.py:30`, `scripts/cohort_attorney_segregate.py:39` |
| F5-6 | **LOW** | **Global API key sharing**: `SALES_OPS_API_KEY` used across all SaaS Admin proxy routes and webhook receivers | `SaaS Admin env.example:148` |
| F5-7 | **INFO** | **No direct tenant DB access from App2**: Confirmed — Sales Ops uses REST API to Supabase, not direct PG connections in TypeScript | No direct PG connections found in TypeScript |
| F5-8 | **INFO** | **No portal holding webhook secrets**: Confirmed — Customer Portal has no webhook-related env vars | Verified |

---

## 6. Handoff Contract Status

### 6.1 Existing Contracts (Legal Product Only)

- `CandidateSubmittedForRepresentationReview` v1 — for INTAKE→RETAINER candidate handoff (10 required fields)
- `ActivateMatterCommand` v1 — for RETAINER→SaaS Admin matter activation (12 required fields)
- `MatterActivatedPayload` v1.0 — for SaaS Admin→TRACE (11 canonical fields)
- `ActivationEvidenceManifest` v1.0 — 9 evidence references

### 6.2 Sales Ops Handoff Contract

**Status: DOES NOT EXIST.** No `SalesOpsApprovedCustomerHandoff` schema exists anywhere. The closest equivalent is the ad-hoc payload in `SaaSAdminWebhookClient.sendApprovedApplication()` which has 10 informal fields, no schema validation, no versioning, and no frozen contract.

---

## 7. Anti-Corruption Mapping Status

**Status: NOT IMPLEMENTED.** No anti-corruption layer exists between Sales Ops and SaaS Admin. The current flow is:

```
Sales Ops SaaSAdminWebhookClient
  → fetch() POST /webhooks/sales-ops/application-approved
    → SaaS Admin creates core_contact directly from Sales Ops payload
      → callback to Sales Ops with contact_id
```

No identity resolution, no deduplication (beyond `source_lead_id` uniqueness), no tenant creation gate, no entitlement configuration from this path. The only provisioning path involves `PlatformServiceClient.createTenant()` which calls `POST /api/v1/tenants` directly.

---

## Summary of All Findings

| Domain | Status | Critical gaps |
|---|---|---|
| Webhook transport | PARTIALLY LIVE | Application-approved webhook works end-to-end but uses simple API key, not HMAC |
| Event envelope | **MISSING** | No Sales Ops event conforms to EventEnvelope v1.0.1 |
| State machine | **MISSING** | Three competing state systems; zero canonical states implemented |
| Pipeline | **DIVERGENT** | TypeScript 16-stage and Python 8-phase completely independent |
| Trust domain | **VIOLATED** | App2 calls App3 directly for tenant provisioning |
| Handoff contract | **MISSING** | No frozen contract exists |
| Anti-corruption | **MISSING** | No boundary layer between Sales Ops and Shared Platform |
| DB constraints | **MISSING** | No enum CHECK constraints on pipeline_stage column |
| Test coverage | **MINIMAL** | 1 Python test file; no TypeScript pipeline tests |
