---
category: decision
title: "PLG-SO-01: Restore STANDARD/SPECIAL_COHORT segmentation"
importance: 8
tags: []
file_paths: []
created: 2026-08-03T19:59:59.739624+00:00
updated: 2026-08-03T19:59:59.739624+00:00
memory_id: f11c99af-84ea-49c2-b73b-16d90e7e57b0
---

# PLG-SO-01: Restore STANDARD/SPECIAL_COHORT segmentation

CTO directive resolved BLOCKER-3 ambiguity: removed sensitive-attribute INFERENCE, preserved SPECIAL_COHORT BUSINESS classification. Migration 179 creates segment_classification columns, special_cohort_pipeline table, campaign_eligibility. Score is now eligibility factor within segment context — not a routing decision. Score >= 70 as sole routing rule REMOVED.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
