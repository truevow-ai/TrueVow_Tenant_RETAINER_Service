---
category: bug
title: "settle_verdicts table never existed + bulk_insert had no validation"
importance: 10
tags: []
file_paths: []
created: 2026-07-09T05:49:06.661351+00:00
updated: 2026-07-09T05:49:06.661351+00:00
memory_id: 6b482af4-193b-467f-aede-26dfabb0d302
---

# settle_verdicts table never existed + bulk_insert had no validation

CRITICAL for a legal-data product: (1) settle_verdicts + settle_verdict_scrape_jobs tables were never migrated - all prior loads 404'd, zero data persisted. (2) app/services/verdict_search.py bulk_insert_verdicts inserts raw dicts with NO validation. (3) scraped enrichment vocab did NOT match DB enums: outcome_type(damages/award/verdict/unspecified vs verdict_plaintiff/defense/settlement/dismissed), liability_tier, plaintiff_age_range, defendant_industry all mismatched; dates were prose not ISO. Fix: verdict_validator.py gate + alembic migration d5e6f7a8b9c0 with CHECK constraints. Loaded 18841 rows. Also batch_load_all globbed base files not *_enriched - would have discarded all enrichment.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
