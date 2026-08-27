---
category: bug
title: "vNext E2E QA - CORE DEFECT: car accident classification"
importance: 8
tags: []
file_paths: []
created: 2026-08-12T15:36:36.068561+00:00
updated: 2026-08-12T15:36:36.068561+00:00
memory_id: bf863927-ad77-4ee8-b772-0e4ae8a36cb1
---

# vNext E2E QA - CORE DEFECT: car accident classification

classify_practice_area keyword list has 'rear ended' (space) but misses 'rear-ended' (hyphen). Common spoken form falls through to default other_personal_injury. File: app/services/benjamin_vnext/lifecycle/lifecycle_fsm.py

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
