# Sales Ops State Conformance Matrix

**Audit date:** 2026-08-01
**Sources:** TypeScript enums/types, Python constants/scripts, database columns, migration files, API validators, tests, UI labels

---

## Complete State Inventory

### 1. `pipeline_stage` Values (Used in `sales_leads` table)

Found in TypeScript `LeadFunnelStage` type (`lib/db/repositories/leads-repository.ts:11-38`) and Zod validator (`app/api/v1/leads/route.ts:22`):

| Value | Canonical equivalent | TypeScript usage | Python usage | DB constraint | UI label |
|---|---|---|---|---|---|
| `scraped` | ❌ None | Active | Active (legacy) | No CHECK | Unknown |
| `enriched` | ❌ None | Active | Active (legacy) | No CHECK | Unknown |
| `outreach_started` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `engaged` | ∼ ENGAGED | Active | Active (legacy) | No CHECK | Unknown |
| `qualified` | ❌ None | Active | Active (legacy) | No CHECK | Unknown |
| `demo_done` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `application_submitted` | ∼ APPLICATION_SUBMITTED | Active | Inactive | No CHECK | Unknown |
| `new` | ❌ None (legacy) | Active | Active (legacy) | No CHECK | Unknown |
| `contacted` | ❌ None (legacy) | Active | Active (legacy) | No CHECK | Unknown |
| `discovery` | ❌ None (legacy) | Active | Active (legacy) | No CHECK | Unknown |
| `demo_booked` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `negotiation` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `kyc_pending` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `kyc_approved` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `application_approved` | ∼ APPROVED_CUSTOMER | Active | Inactive | No CHECK | Unknown |
| `provisioning` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `won` | ❌ None (legacy) | Active | Active (legacy) | No CHECK | Unknown |
| `converted` | ∼ HANDED_OFF | Active (set by `updateLeadWithContactId`) | Inactive | No CHECK | Unknown |
| `lost` | ❌ None (legacy) | Active | Active (legacy) | No CHECK | Unknown |
| `disqualified` | ∼ SUPPRESSED | Active | Inactive | No CHECK | Unknown |
| `rejected` | ∼ REJECTED | Active | Inactive | No CHECK | Unknown |
| `waitlist` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `customer` | ❌ None | Active | Inactive | No CHECK | Unknown |
| `cohort_pending` | ❌ None | Active (set by Website Intake manager) | Inactive | No CHECK | Unknown |
| `enrichment_pending` | ❌ None | Active (set by Website Intake manager) | Inactive | No CHECK | Unknown |

### 2. `PipelineStage` Enum Values (Lead Factory — `lib/lead-factory/types.ts`)

| Value | Canonical equivalent | PipelineStateManager validation | UI label |
|---|---|---|---|
| `market_planned` | ❌ None | ✅ Validated | Unknown |
| `scouted` | ❌ None | ✅ Validated | Unknown |
| `identity_normalized` | ∼ NORMALIZED | ✅ Validated | Unknown |
| `website_profiled` | ∼ PROFILED | ✅ Validated | Unknown |
| `contact_enriched` | ✅ CONTACT_ENRICHED | ✅ Validated | Unknown |
| `enriched_deep` | ❌ None | ✅ Validated | Unknown |
| `contact_validated` | ❌ None | ✅ Validated | Unknown |
| `signal_scored` | ∼ SCORED | ✅ Validated | Unknown |
| `quality_gated` | ❌ None | ✅ Validated | Unknown |
| `qa_audited` | ∼ QA_PENDING | ✅ Validated | Unknown |
| `outreach_angle_generated` | ❌ None | ✅ Validated | Unknown |
| `ingested` | ❌ None | ✅ Validated | Unknown |
| `campaign_ready` | ∼ CAMPAIGN_ELIGIBLE | ✅ Validated (terminal) | Unknown |
| `pending_sania_review` | ❌ None | ✅ Validated | Unknown |
| `sania_approved` | ❌ None | ✅ Validated | Unknown |
| `sania_rejected` | ❌ None | ✅ Validated (terminal) | Unknown |
| `failed` | ❌ None | ✅ Validated | Unknown |
| `quarantined` | ❌ None | ✅ Validated (terminal or retry) | Unknown |

### 3. Python 8-Phase Pipeline (`scripts/pipeline_phases.py`)

| Phase | Stages from `run_state_pipeline.py` STEPS | DB batch tracking |
|---|---|---|
| 1. Lead Search & Scraping | Scrapers (FL, CA, TX, GA, etc.) | `batch_id` column |
| 2. Law Firm Information Gathering | Website crawling (phase2) | `batch_id` column |
| 3. Attorney Extraction | `attorney_enrich.py`, `build_standard_attorney_leads.py` | `batch_id` column |
| 4. Contact Discovery | `verify_emails_phones.py`, `classify_phone_types.py`, `verify_attorney_emails.py`, `segment_standard_outreach.py`, `segment_floor_outreach.py` | `batch_id` column |
| 5. DeepSeek Primary Enrichment | `enrich_backfill.py`, `deepseek_enrich.py` | Checkpoint JSON files |
| 6. Gemini Secondary Enrichment | `enrich_backfill.py` (browser fallback), `propagate_sibling_enrichment.py` | Checkpoint JSON files |
| 7. Firm-Level Cohort Segregation | `cohort_firm_tag.py`, `cohort_firm_segregate.py` | `community_tag`, `cohort_tier` columns |
| 8. Attorney-Level Cohort Segregation | `cohort_attorney_segregate.py` | `attorney_cohort_leads` table |

---

## Conflicts and Inconsistencies

### Duplicate states (different names, same meaning)

| State 1 | State 2 | Source 1 | Source 2 | Action |
|---|---|---|---|---|
| `application_approved` | `APPROVED_CUSTOMER` (canonical) | TS-LEADS | Canonical | Rename TS-LEADS value |
| `converted` | `HANDED_OFF` (canonical) | TS-LEADS | Canonical | Rename TS-LEADS value |
| `engaged` | `ENGAGED` (canonical) | TS-LEADS | Canonical | Case-normalize |
| `application_submitted` | `APPLICATION_SUBMITTED` (canonical) | TS-LEADS | Canonical | Case-normalize |
| `identity_normalized` | `NORMALIZED` (canonical) | TS-FACTORY | Canonical | Rename TS-FACTORY value |
| `website_profiled` | `PROFILED` (canonical) | TS-FACTORY | Canonical | Rename TS-FACTORY value |
| `signal_scored` | `SCORED` (canonical) | TS-FACTORY | Canonical | Rename TS-FACTORY value |
| `qa_audited` | `QA_PENDING` (canonical) | TS-FACTORY | Canonical | Different meaning — QA_AUDITED is post-review; QA_PENDING is pre-review |
| `campaign_ready` | `CAMPAIGN_ELIGIBLE` (canonical) | TS-FACTORY | Canonical | Rename TS-FACTORY value |

### Conflicting names (same name, different meaning)

| Name | Meaning in TS-LEADS | Meaning in TS-FACTORY | Meaning in PY |
|---|---|---|---|
| (No conflicts found — no state name is shared across systems with different meanings) | — | — | — |

### States used only in UI (not backed by DB constraint)

None identified — the UI appears to consume DB values directly via the leads API.

### States used only in scripts (not in TypeScript)

- `cohort_pending`, `enrichment_pending` — set only by `WebsiteIntakeManager`
- Python Phase 7+8 states — tracked via `community_tag` and `cohort_tier` columns, not `pipeline_stage`

### Code values not allowed by DB

**All 25 `pipeline_stage` values are permitted** because the column has no CHECK or ENUM constraint. Any string can be inserted.

### DB values not represented in code

Cannot verify without live DB access — requires `SELECT DISTINCT pipeline_stage FROM sales_leads;` to detect undocumented stage values.

---

## Recommended Canonical Mapping

The existing values should be consolidated into the canonical Sales Ops lifecycle:

```
Legacy/Current     →  Canonical
─────────────────────────────────
new, discovery      →  DISCOVERED
scraped             →  (remove — use batch_id tracking instead)
identity_normalized →  NORMALIZED
website_profiled    →  PROFILED
contact_enriched    →  CONTACT_ENRICHED
contact_validated   →  VALIDATION_PENDING (rename to match canonical intent)
enriched_deep       →  PROFILED (enrichment happens in PROFILED phase)
enriched            →  PROFILED
email_verified=true →  VERIFIED (promote from BOOLEAN to lifecycle state)
signal_scored       →  SCORED
quality_gated       →  QA_PENDING (rename — gating is pre-QA, not post)
qa_audited          →  (keep as QA_PENDING sub-state, not main state)
outreach_angle_generated → (demote to enrichment attribute, not state)
ingested            →  CAMPAIGN_ELIGIBLE (rename)
campaign_ready      →  CAMPAIGN_ELIGIBLE
outreach_started    →  IN_CAMPAIGN (rename)
engaged             →  ENGAGED
application_submitted → APPLICATION_SUBMITTED
qualified           →  QUALIFICATION_REVIEW (rename)
application_approved → APPROVED_CUSTOMER
converted           →  HANDED_OFF
provisioning        →  (remove — belongs to SaaS Admin, not Sales Ops)
won, lost, waitlist →  (demote to outcome fields, not pipeline_stage)
customer            →  (remove — replaced by APPROVED_CUSTOMER)
cohort_pending      →  (demote to enrichment attribute, not state)
enrichment_pending  →  (demote to enrichment attribute, not state)
kyc_pending         →  (demote to KYC service sub-state)
kyc_approved        →  (demote to KYC service sub-state)
demo_booked         →  (demote to activity, not pipeline_stage)
demo_done           →  (demote to activity, not pipeline_stage)
negotiation         →  (remove — legacy sales CRM concept)
rejected            →  REJECTED
disqualified        →  SUPPRESSED
market_planned      →  (remove — campaign planning, not lead lifecycle)
scouted             →  DISCOVERED (merge into canonical DISCOVERED)
failed              →  FAILED (add to canonical as error branch)
quarantined         →  FAILED (sub-state of FAILED)
pending_sania_review → (demote to HITL status attribute)
sania_approved      →  (demote to HITL status attribute)
sania_rejected      →  (demote to HITL status attribute)
```
