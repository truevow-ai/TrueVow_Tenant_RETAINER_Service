---
category: bug
title: "Phase 3 checkpoint marks done regardless of extraction success"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T06:42:19.534271+00:00
updated: 2026-07-08T06:42:19.534271+00:00
memory_id: d755395b-e5aa-4aec-ad01-240325ed49f3
---

# Phase 3 checkpoint marks done regardless of extraction success

attorney_enrich.py adds index to checkpoint even when extract_attorneys returns None/empty. Stale Jul-1 checkpoint had all 2526 marked done, blocking re-runs. Rebuilt checkpoint to retry firms with website but empty firm_attorneys. Also: CA leads (0 in DB) counted in the 2526 total via old run - checkpoint index misalignment risk.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
