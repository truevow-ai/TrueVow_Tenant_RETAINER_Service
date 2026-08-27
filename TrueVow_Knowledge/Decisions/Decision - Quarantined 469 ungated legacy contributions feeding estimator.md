---
category: decision
title: "Quarantined 469 ungated legacy contributions feeding estimator"
importance: 10
tags: []
file_paths: []
created: 2026-07-11T01:35:38.675032+00:00
updated: 2026-07-11T01:35:38.675032+00:00
memory_id: 680698cf-50fc-4274-8330-848f1f1e3319
---

# Quarantined 469 ungated legacy contributions feeding estimator

settle_contributions held 469 rows from a single 2026-05-11 ungated seed batch (seed-via-supabase-client.py, bypassing gates): 0 contributor_user_id, 0 blockchain_hash, 0 source_type, 0 exact_outcome_amount - no provenance. They were live-feeding SettlementEstimator via status=approved. Quarantined all (status->pending, is_outlier=true, confidence=0, rejection_reason) - preserved for re-verification, never destroyed. Estimator now 0 approved -> graceful insufficient_data. Also kill-switched 24 ungated scripts + launcher. Zero honest output > fabricated estimates.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
