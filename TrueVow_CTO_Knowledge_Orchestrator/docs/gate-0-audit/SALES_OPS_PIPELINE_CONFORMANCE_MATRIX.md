# Sales Ops Pipeline Conformance Matrix

**Audit date:** 2026-08-01
**Canonical pipeline:** Sales Ops Stabilization Plan Section 4.3 — 18-stage lifecycle + branches

---

## Methodology

Each canonical stage is compared against three implementation sources:
- **TS-LEADS**: `LeadFunnelStage` type in `lib/db/repositories/leads-repository.ts`
- **TS-FACTORY**: `PipelineStage` enum in `lib/lead-factory/types.ts`
- **PY**: Python `pipeline_phases.py` PHASES dictionary + script implementations

Key: ✅ = Found, ∼ = Approximate equivalent, ❌ = Not found, — = N/A

---

## Conformance Matrix

| # | Canonical Stage | TS-LEADS | TS-FACTORY | PY | Notes |
|---|---|---|---|---|---|
| C1 | DISCOVERED | ❌ | ❌ | ❌ | `discovery` exists as legacy string but not canonical `DISCOVERED` |
| C2 | NORMALIZED | ❌ | `IDENTITY_NORMALIZED` ∼ | ❌ | Different stage name; same intent (name normalization) |
| C3 | PROFILED | ❌ | `WEBSITE_PROFILED` ∼ | ✅ Phase 2 "Firm Information Gathering" | Python Phase 2 crawls websites for firmographics |
| C4 | CONTACT_ENRICHED | ❌ | `CONTACT_ENRICHED` ✅ | ✅ Phase 4 "Contact Discovery" | Python Phase 4 discovers emails + phones + SMTP verify |
| C5 | VALIDATION_PENDING | ❌ | ❌ | ❌ | No explicit validation-pending state anywhere |
| C6 | VERIFIED | ❌ | ❌ | ❌ | No explicit verified state; `email_verified` is a BOOLEAN field |
| C7 | SCORED | ❌ | `SIGNAL_SCORED` ∼ | ❌ | TS-Factory "signal scoring" maps to assessment, not lead_score |
| C8 | QA_PENDING | ❌ | `QA_AUDITED` ∼ | ❌ | `QA_AUDITED` is post-audit, not pending-audit |
| C9 | OUTREACH_APPROVED | ❌ | ❌ | ❌ | `OUTREACH_ANGLE_GENERATED` exists but is content creation, not approval |
| C10 | CAMPAIGN_ELIGIBLE | ❌ | `CAMPAIGN_READY` ∼ | ❌ | Similar concept — lead is ready for campaign ingestion |
| C11 | IN_CAMPAIGN | ❌ | ❌ | ❌ | No campaign assignment state |
| C12 | ENGAGED | `engaged` ✅ | ❌ | ❌ | String literal in `LeadFunnelStage` type; no enum |
| C13 | APPLICATION_STARTED | ❌ | ❌ | ❌ | No pre-submission application state |
| C14 | APPLICATION_SUBMITTED | `application_submitted` ✅ | ❌ | ❌ | String literal; no enum constraint |
| C15 | QUALIFICATION_REVIEW | ❌ | ❌ | ❌ | No qualification-review state |
| C16 | APPROVED_CUSTOMER | `application_approved` ✅ | ❌ | ❌ | String literal; `ApplicationDecision = 'approved'` exists |
| C17 | HANDOFF_PENDING | ❌ | ❌ | ❌ | No handoff-pending state; handoff is fire-and-forget |
| C18 | HANDED_OFF | `converted` ✅ | ❌ | ❌ | Set by `updateLeadWithContactId()` after SaaS Admin callback |

### Branch States

| Branch | TS-LEADS | TS-FACTORY | PY | Notes |
|---|---|---|---|---|
| REJECTED | `rejected` ✅ | `SANIA_REJECTED` ❌ (different concept) | ❌ | `rejected` exists as string in leads API |
| SUPPRESSED | `disqualified` ✅ | ❌ | ❌ | `do_not_outreach` BOOLEAN field exists |
| REMEDIATION_REQUIRED | ❌ | ❌ | ❌ | No remediation state |
| UNRESPONSIVE | ❌ | ❌ | ❌ | No unresponsive tracking |
| FAILED | ❌ | `FAILED` ✅ | ❌ | `FAILED` → `QUARANTINED` path in factory |

---

## Summary Statistics

| Source | States defined | Matching canonical | Approximate match | Missing canonical |
|---|---|---|---|---|
| TS-LEADS (`LeadFunnelStage`) | 21 string values | 4 (engaged, application_submitted, application_approved, converted) | 0 | 14 |
| TS-FACTORY (`PipelineStage`) | 16 enum values | 1 (CONTACT_ENRICHED) | 5 | 12 |
| PY (`pipeline_phases.py`) | 8 phases | 0 | 2 (PROFILED, CONTACT_ENRICHED) | 16 |

### Cross-Source Alignment

| Canonical Stage | Aligned across sources? |
|---|---|
| CONTACT_ENRICHED | ✅ TS-FACTORY + PY both have equivalents |
| PROFILED | ∼ PY has equivalent; TS-FACTORY has `WEBSITE_PROFILED` |
| All other 16 stages | ❌ No cross-source alignment |

---

## Implementation Gaps

| Category | Count | Details |
|---|---|---|
| States missing from ALL sources | 12 | DISCOVERED, VALIDATION_PENDING, VERIFIED, OUTREACH_APPROVED, IN_CAMPAIGN, APPLICATION_STARTED, QUALIFICATION_REVIEW, HANDOFF_PENDING + remediation branches |
| States present in code but not canonical | 20+ | `scraped`, `new`, `contacted`, `discovery`, `demo_booked`, `demo_done`, `negotiation`, `won`, `lost`, `waitlist`, `customer`, `provisioning`, `cohort_pending`, `enrichment_pending`, `MARKET_PLANNED`, `SCOUTED`, `ENRICHED_DEEP`, `QUALITY_GATED`, `OUTREACH_ANGLE_GENERATED`, `INGESTED`, `PENDING_SANIA_REVIEW`, `QUARANTINED` |
| DB constraints on states | 0 | No CHECK or ENUM constraint on `pipeline_stage` column |
| State transition validation | PARTIAL | Only in TS-FACTORY `PipelineStateManager`; no transition validation in TS-LEADS or PY |
| Idempotent state transitions | 0 | No idempotency keys for state changes |
