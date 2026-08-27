---
category: architecture
title: "PLG-SO-01: Segmentation restored \u2014 STANDARD vs SPECIAL_COHORT"
importance: 9
tags: []
file_paths: []
created: 2026-08-05T07:37:29.034362+00:00
updated: 2026-08-05T07:37:29.034362+00:00
memory_id: 2b8e6c63-8a22-465c-84dc-0d308c7a4b39
---

# PLG-SO-01: Segmentation restored — STANDARD vs SPECIAL_COHORT

Removed score-only routing (score>=70 → IN_CAMPAIGN). Segment is routing key, score is eligibility factor. Migration 179 adds segment_code, classification_status, special_cohort_pipeline table. SegmentClassifier, CampaignEligibilityEvaluator, SpecialCohortPipeline services created. 48 tests PASS.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
