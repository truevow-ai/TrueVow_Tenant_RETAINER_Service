---
category: decision
title: "PLG-SO-01A: REVIEW_REQUIRED default \u2014 never fallback STANDARD"
importance: 9
tags: []
file_paths: []
created: 2026-08-05T07:37:32.790341+00:00
updated: 2026-08-05T07:37:32.790341+00:00
memory_id: 8c3ece73-0386-45f7-96f2-07b85c908c5c
---

# PLG-SO-01A: REVIEW_REQUIRED default — never fallback STANDARD

Corrected Phase 4 backfill: unresolved leads → REVIEW_REQUIRED, not STANDARD. Firm-name matching requires corroboration (state/website/email). Migration 180 idempotent safety correction. CampaignEligibilityEvaluator enforces classification_status ≠ CLASSIFIED → HELD. Evidence strength model: authoritative vs supporting vs insufficient.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
