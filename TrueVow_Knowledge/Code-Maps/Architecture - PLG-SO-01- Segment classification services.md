---
category: architecture
title: "PLG-SO-01: Segment classification services"
importance: 8
tags: []
file_paths: []
created: 2026-08-03T20:00:02.951429+00:00
updated: 2026-08-03T20:00:02.951429+00:00
memory_id: 58bc145b-becc-4be1-9037-3a0d3431fce7
---

# PLG-SO-01: Segment classification services

Created SegmentClassifier (governed classification with audit trail), CampaignEligibilityEvaluator (segment+lifecycle+suppression checks), SpecialCohortPipeline (8-status management pipeline), ApplicationRouter (segment-aware routing), HandoffGuard (6 negative proofs). All write to lead_segment_classifications audit table.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
