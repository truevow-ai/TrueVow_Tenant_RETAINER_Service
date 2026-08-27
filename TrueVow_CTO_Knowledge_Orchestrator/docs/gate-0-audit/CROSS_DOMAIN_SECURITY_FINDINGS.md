# Cross-Domain Security Findings — Sales Ops Gate 0

**Audit date:** 2026-08-01
**Trust domains:** App1 (PLATFORM_OPERATORS), App2 (SALES_SUPPORT), App3 (TENANTS)
**Repositories:** `TrueVow_Sales_Ops_Service`, `TrueVow_SaaS_Administration_Service`

---

## Finding 1: App2 Writing Directly to App3

**Severity:** HIGH
**Repository:** `TrueVow_Sales_Ops_Service`
**File:** `lib/integrations/tenant-application-service.ts:232`
**Code:** `POST /api/v1/tenants/provision` (Sales Ops → INTAKE Service)

**Description:** Sales Ops (App2, MEDIUM trust) calls the INTAKE tenant provisioning endpoint (App3, EXTERNAL) directly. This violates the trust-domain boundary: App2 services should not write to App3 services. Tenant provisioning should only be triggered by SaaS Admin (App1) after receiving the handoff package from Sales Ops.

**Required owner:** Ghaus-FSD (Sales Ops), Ghous-ISB (SaaS Admin)
**Required correction:** Remove `tenantClient.provisionTenant()` from Sales Ops `LeadPromotionService`. Move tenant provisioning to SaaS Admin's handoff consumer.

---

## Finding 2: Simple API Key Auth on Webhook (Not HMAC)

**Severity:** MEDIUM
**Repository:** `TrueVow_Sales_Ops_Service`
**File:** `lib/integrations/saas-admin/webhook-client.ts:49-67`
**Code:** `'X-API-Key': this.apiKey` — plain string comparison on receiver side

**Description:** The application-approved webhook uses simple `X-API-Key` header comparison instead of HMAC-SHA256 signing (WebhookSignature v1.0). The frozen WebhookSignature v1.0 contract requires HMAC-SHA256 with `X-TrueVow-Key-Id`, `X-TrueVow-Timestamp`, `X-TrueVow-Signature` headers for all cross-service webhooks. The legacy bearer auth cutoff is 2026-09-01.

**Required owner:** Ghaus-FSD (Sales Ops), Ghous-ISB (SaaS Admin)
**Required correction:** Upgrade to HMAC-SHA256 signing on both sender and receiver sides per WebhookSignature v1.0.

---

## Finding 3: No Idempotency Key on Handoff Call

**Severity:** MEDIUM
**Repository:** `TrueVow_Sales_Ops_Service`
**File:** `lib/integrations/saas-admin/webhook-client.ts:63`
**Code:** `'X-Request-ID': \`sales-ops-${Date.now()}-${payload.lead_id?.slice(0, 8)}\`` — uses Date.now() which is NOT deterministic

**Description:** Retrying the same `sendApprovedApplication()` call generates a different `X-Request-ID` because it includes `Date.now()`. The receiver (SaaS Admin) relies on `core_contacts.source_lead_id` uniqueness for idempotency, which handles duplicates at the DB level but silently creates an inconsistent contract — the sender cannot correlate a retry to the same logical event.

**Required owner:** Ghaus-FSD (Sales Ops)
**Required correction:** Use a stable idempotency key derived from `lead_id + handoff_version` or a dedicated `event_id` UUID.

---

## Finding 4: Sensitive-Attribute Inference in Production Pipeline

**Severity:** HIGH (compliance)
**Repository:** `TrueVow_Sales_Ops_Service`
**Files:** `scripts/cohort_firm_tag.py`, `scripts/cohort_firm_segregate.py`, `scripts/cohort_attorney_segregate.py`
**Data:** `scripts/scrapers/name_ethnicity_lookup.json` (5000+ entries)

**Description:** The Python pipeline infers community affiliation (jewish, hispanic, muslim, asian, indian, catholic, orthodox, mormon) from attorney and firm names using a lookup table. This is mandatory cohorting stage (Phase 7 + Phase 8) built into the pipeline. This constitutes sensitive-attribute inference without:
- Documented lawful purpose
- Legal review
- Privacy review
- Approved source policies
- Correction and deletion procedures

The Sales Ops Stabilization Plan Section 3.1 explicitly mandates removal of this from the default pipeline.

**Required owner:** Sania (Sales Ops Chief of Staff)
**Required correction:** Remove Phase 7 and Phase 8 from the default pipeline. Replace with optional Affinity/Community Program Eligibility using defensible criteria (explicitly declared affiliation, public business-directory membership, voluntary program participation).

---

## Finding 5: Global API Key Shared Across Services

**Severity:** LOW
**Repository:** `TrueVow_SaaS_Administration_Service`
**File:** `env.example:148`
**Code:** `SALES_OPS_SERVICE_API_KEY=sk_live_your_sales_ops_api_key` — same key used for all Sales Ops → SaaS Admin calls

**Description:** A single API key is used for all Sales Ops → SaaS Admin interactions (proxy routes, webhook receivers). If this key leaks, all cross-service calls from Sales Ops to SaaS Admin are compromised. Per the platform's security architecture, each caller-receiver relationship should have its own key.

**Required owner:** Ghous-ISB (SaaS Admin)
**Required correction:** Implement per-path API key isolation. At minimum, separate keys for webhook receiver vs. proxy routes.

---

## Finding 6: No Firm/Tenant Scoping on Sales Ops → SaaS Admin Proxy Routes

**Severity:** MEDIUM
**Repository:** `TrueVow_SaaS_Administration_Service`
**Files:** `app/api/v1/sales-ops/leads/route.ts`, `app/api/v1/sales/stats/route.ts`
**Code:** Proxy routes pass through API key auth but apply no tenant or firm scoping

**Description:** Proxy routes that forward Sales Ops requests to the SaaS Admin backend use only `X-API-Key` auth with no tenant-scoping or firm-scoping. If the API key is compromised, the attacker can query any lead or stat.

**Required owner:** Ghous-ISB (SaaS Admin)
**Required correction:** Add firm-scope validation on proxy routes. Sales Ops should only access leads/stats scoped to known Sales Ops tenant identifiers.

---

## Finding 7: No Audit Entries for Cross-Domain Calls

**Severity:** LOW
**Repository:** Both
**Files:** All cross-domain integration clients in `lib/integrations/`

**Description:** Cross-domain HTTP calls from Sales Ops to SaaS Admin, CS-Support, and Tenant App are made without emitting audit events on the calling side. The SaaS Admin receiver does log to `system_audit_log` for some operations, but there is no audit trail on the Sales Ops sender side for cross-service operations.

**Required owner:** Ghaus-FSD (Sales Ops)
**Required correction:** Add audit events with `actor_type`, `actor_id`, `authority_class` to all cross-domain HTTP calls from Sales Ops.

---

## Finding 8: No Direct Tenant DB Access from App2 (CONFIRMED SAFE)

**Status:** **NO VIOLATION FOUND.** Sales Ops TypeScript code uses Supabase REST API calls to its own database only. Python scripts use direct `psycopg2`/`asyncpg` connections to `SALES_OPS_DATABASE_URL`. No cross-service direct DB access detected.

---

## Finding 9: No Portal Holding Webhook Secrets (CONFIRMED SAFE)

**Status:** **NO VIOLATION FOUND.** Customer Portal (App3) has no webhook secret env vars or signing capabilities. Webhook secrets are scoped to backend services only.

---

## Finding 10: Python Scripts Connect Directly to Supabase with Service Role Key

**Severity:** LOW
**Repository:** `TrueVow_Sales_Ops_Service`
**Files:** `scripts/tx_pipeline_rest.py:45-79`, `scripts/segment_floor_outreach.py:37-51`, `scripts/enrich_backfill_rest.py:48-59`

**Description:** Python batch scripts use `SUPABASE_SERVICE_ROLE_KEY` over REST API to bypass RLS. This is acceptable for offline batch processing but the service role key should be scoped to batch operations only and never used in runtime request paths.

**Required owner:** Ghaus-FSD (Sales Ops)
**Required correction:** Confirm service role key is NOT used in any Next.js API route handler. (Verified: it is not.)

---

## Summary

| Severity | Count | Items |
|---|---|---|
| HIGH | 2 | F1 (App2→App3 write), F4 (sensitive-attribute inference) |
| MEDIUM | 3 | F2 (simple API key), F3 (non-deterministic idempotency), F6 (no firm scoping) |
| LOW | 3 | F5 (global API key), F7 (no audit entries), F10 (service role key in batch) |
| SAFE | 2 | F8 (no direct tenant DB), F9 (no portal secrets) |

### Top Priorities for Remediation

1. **F4**: Remove sensitive-attribute inference from production pipeline (compliance blocker)
2. **F1**: Remove App2→App3 direct provisioning call; route through SaaS Admin
3. **F2**: Upgrade application-approved webhook to HMAC-SHA256 (before 2026-09-01 cutoff)
