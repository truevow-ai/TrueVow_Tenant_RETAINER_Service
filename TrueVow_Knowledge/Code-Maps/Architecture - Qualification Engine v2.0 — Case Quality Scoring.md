---
category: architecture
title: "Qualification Engine v2.0 \u2014 Case Quality Scoring"
importance: 9
tags: []
file_paths: []
created: 2026-07-30T04:01:50.246019+00:00
updated: 2026-07-30T04:01:50.246019+00:00
memory_id: 7c2f89f5-088a-408d-863e-e03444e7e9d4
---

# Qualification Engine v2.0 — Case Quality Scoring

Refactored from intake-completeness scoring to case-opportunity scoring. Two independent scores: case_quality (0-100) and intake_completion (0-100%). 7 categories totaling 100 pts: Liability 30, Injury 25, Treatment 15, Evidence 10, Insurance 10, Damages 5, Client Fit 5. Starting score 0 (earned, not deducted). Confidence-weighted: category points multiplied by avg confidence of matched fields. Penalties: statute -20/-50, represented -40, no injury -25. Grade: A+ 90, A 75, B 55, C 35, D 0. Priority: immediate/24h/review/nurture/decline. Rules in config/qualification/personal_injury_v2.yaml. Backward compatible. Test: fracture+police+full insurance = 98 A+ immediate.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
