---
category: decision
title: "PLG-SO-01A: Corrected default STANDARD \u2192 REVIEW_REQUIRED"
importance: 9
tags: []
file_paths: []
created: 2026-08-03T20:32:02.458864+00:00
updated: 2026-08-03T20:32:02.458864+00:00
memory_id: 2409504e-c53b-4de6-9ef3-f7106dd5254c
---

# PLG-SO-01A: Corrected default STANDARD → REVIEW_REQUIRED

Migration 179 Phase 4 corrected: unresolved leads default to REVIEW_REQUIRED, not STANDARD. Firm-name matching requires corroboration (state/website/email). Migration 180 provides idempotent forward safety correction. REVIEW_REQUIRED → campaign HELD enforced before score/cadence/region evaluation. Classification provenance recorded on every record. v_classification_review_queue created.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
