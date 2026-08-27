# Implementation Order — Gate 0R (Revised)

**Revised:** 2026-08-01
**Supersedes:** Previous IMPLEMENTATION_ORDER_AND_DEPENDENCIES.md
**Decision:** CONDITIONAL GO — BLOCKER REMEDIATION ONLY

---

## Revised Execution Order

Work is restricted to blocker resolution only. State migration, new features, and production rollout are NOT authorized.

```
Phase 0: CRITICAL BLOCKERS (must complete before any further work)
├── B0 — Disable direct App2 → App3 provisioning path
├── B3 — Remove sensitive-attribute phases from production execution
├── B1 — Freeze EventEnvelope v1.1.0
└── B2 — Freeze Sales Ops lifecycle and transition registries

Phase 1: HIGH BLOCKERS (may begin after Phase 0 criticals are closed)
├── B6 — Freeze SalesOpsApprovedCustomerHandoff v1.0.0
├── B4 — Replace API-key-only webhook auth with HMAC-SHA256
├── B5 — Correct verified architecture documentation
└── B7 — Implement canonical Sales Ops event builder

Phase 2: GATE 0R REASSESSMENT
├── Rerun all 43 commissioning tests
├── Verify 15 blocker acceptance tests
└── Issue CTO_GATE_0_REASSESSMENT.md

Phase 3: STATE MIGRATION (requires GO decision from Phase 2)
├── Migrate pipeline_stage to canonical states
├── Deprecate legacy CRM pipeline stages
└── Add DB CHECK constraints

Phase 4: FULL IMPLEMENTATION (requires GO decision)
├── Sales Ops ontology embedding
├── SaaS Admin handoff consumer
├── Tenant creation from handoff
├── Entitlement configuration
└── End-to-end commissioning
```

---

## Phase 0: Critical Blockers — Detailed Tasks

### B0: Disable App2 → App3 Provisioning

| Step | Action | File | Owner |
|---|---|---|---|
| B0.1 | Guard `provisionTenant()` call in `LeadPromotionService` | `lib/services/lead-promotion-service.ts` | Ghaus-FSD |
| B0.2 | Add architecture gate test preventing App2→App3 calls | `__tests__/architecture/app2-app3-boundary.test.ts` | Ghaus-FSD |
| B0.3 | Confirm handoff flow terminates at SaaS Admin webhook | `lib/integrations/saas-admin/webhook-client.ts` | Ghaus-FSD |

### B3: Remove Sensitive-Attribute Phases

| Step | Action | File | Owner |
|---|---|---|---|
| B3.1 | Mark phases 7-8 DEPRECATED in pipeline definition | `scripts/pipeline_phases.py` | ✅ DONE |
| B3.2 | Remove phases 7-8 from pipeline runner | `scripts/run_state_pipeline.py` | Ghaus-FSD |
| B3.3 | Update COMPLETENESS_CHECKLIST | `scripts/pipeline_phases.py` | ✅ DONE |
| B3.4 | Add test proving pipeline works without phases 7-8 | `scripts/tests/pipeline_no_sensitive_inference.py` | Ghaus-FSD |
| B3.5 | Produce removal report | `docs/SENSITIVE_ATTRIBUTE_PIPELINE_REMOVAL_REPORT.md` | Ghaus-FSD |

### B1: EventEnvelope v1.1.0

| Step | Action | File | Owner |
|---|---|---|---|
| B1.1 | JSON Schema v1.1.0 published | `contracts/event-envelope.schema.json` | ✅ DONE |
| B1.2 | TypeScript interface updated | `lib/contracts/index.ts` | ✅ DONE |
| B1.3 | Golden fixtures updated for v1.1.0 | `supabase/migrations/173_final_contract_fixes.sql` | Ghous-ISB |
| B1.4 | Python models generated | to be created | CTO |
| B1.5 | Version compatibility matrix | to be created | CTO |

### B2: Sales Ops Lifecycle Freeze

| Step | Action | File | Owner |
|---|---|---|---|
| B2.1 | Canonical ontology YAML published | `TrueVow_Sales_Ops_Ontology_Registry_v1.0.yaml` | ✅ DONE |
| B2.2 | Lead state registry | to be created | CTO + Sales Ops |
| B2.3 | Application state registry | to be created | CTO + Sales Ops |
| B2.4 | Transition registry | to be created | CTO + Sales Ops |
| B2.5 | Reason code registry | to be created | CTO + Sales Ops |
| B2.6 | Legacy state mapping | to be created | CTO + Sales Ops |

---

## Phase 1: High Blockers — Detailed Tasks

### B6: Handoff Contract Freeze

| Step | Action | File | Owner |
|---|---|---|---|
| B6.1 | Review generated schema | `SALES_OPS_HANDOFF_CONTRACT_V1.schema.json` | ✅ DONE (generated) |
| B6.2 | CTO approval | — | Yasha |
| B6.3 | Version as v1.0.0 | — | CTO |

### B4: HMAC Webhook Upgrade

| Step | Action | File | Owner |
|---|---|---|---|
| B4.1 | Sales Ops sender: implement HMAC signing | `lib/integrations/saas-admin/webhook-client.ts` | Ghaus-FSD |
| B4.2 | SaaS Admin receiver: implement HMAC verification | `app/api/v1/webhooks/sales-ops/application-approved/route.ts` | Ghous-ISB |
| B4.3 | Key registry entry added | `lib/security/webhook-auth.ts` | Ghous-ISB |
| B4.4 | TypeScript golden tests | `__tests__/security/webhook-signature.test.ts` (Sales Ops) + `tests/security/sales-ops-webhook-signature.test.ts` (SaaS Admin) | Both |

### B5: Documentation Correction

| Step | Action | File | Owner |
|---|---|---|---|
| B5.1 | Mark tenant.created as LIVE | `Cross-Service/service-dependency-map.md` | ✅ DONE |
| B5.2 | Mark sync_lead as LIVE | `Cross-Service/service-dependency-map.md` | ✅ DONE |
| B5.3 | Add Sales Ops→CS-Support flow | `Cross-Service/service-dependency-map.md` | ✅ DONE |
| B5.4 | Add App2→App3 violation note | `Cross-Service/service-dependency-map.md` | ✅ DONE |

### B7: Canonical Event Builder

| Step | Action | File | Owner |
|---|---|---|---|
| B7.1 | TypeScript event builder | `lib/events/event-builder.ts` | Ghaus-FSD |
| B7.2 | Python event builder | `scripts/events/event_builder.py` | Ghaus-FSD |
| B7.3 | TypeScript golden tests | `__tests__/events/event-builder.test.ts` | Ghaus-FSD |
| B7.4 | Python golden tests | `scripts/tests/event_builder_test.py` | Ghaus-FSD |

---

## Blockers Already Resolved

| Blocker | Status | Evidence |
|---|---|---|
| B5 (stale documentation) | ✅ RESOLVED | `service-dependency-map.md` updated |
| B3 Phase 1 (mark pipeline deprecated) | ✅ RESOLVED | `pipeline_phases.py` phases 7-8 marked DEPRECATED; COMPLETENESS_CHECKLIST updated |
| B1 Phase 1 (EventEnvelope v1.1.0 schema + TS) | ✅ RESOLVED | JSON Schema and TypeScript interface updated |
| B2 Phase 1 (ontology YAML) | ✅ RESOLVED | `TrueVow_Sales_Ops_Ontology_Registry_v1.0.yaml` created |

---

## Remaining Blocker Work

| Blocker | Remaining work | Owner |
|---|---|---|
| B0 | Disable `provisionTenant()`, add architecture test | Ghaus-FSD (Sales Ops) |
| B1 | Golden fixture update, Python models, compatibility matrix | CTO + Ghous-ISB |
| B2 | State/transition/reason-code registries, legacy mapping | CTO + Sales Ops |
| B3 | Remove from pipeline runner, add test, produce report | Ghaus-FSD (Sales Ops) |
| B4 | HMAC sender + receiver + key registry + golden tests | Ghaus-FSD + Ghous-ISB |
| B6 | CTO review and approval | Yasha |
| B7 | Event builders (TS + PY) + golden tests | Ghaus-FSD (Sales Ops) |
