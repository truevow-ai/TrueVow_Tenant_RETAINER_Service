---
category: architecture
title: "workflow co-ownership model for bridge agents"
importance: 9
tags: []
file_paths: []
created: 2026-07-16T08:54:33.308747+00:00
updated: 2026-07-16T08:54:33.308747+00:00
memory_id: cf8f3b6e-f4d7-42f5-9904-bbfa76fc3b8f
---

# workflow co-ownership model for bridge agents

While the canonical workflow template is still under active development, a sequential-edit protocol applies: ONE designated agent edits personal_injury_speech.json + workflow_engine.py at a time. Bridge agents work on bridge files only. If they need engine/workflow changes, they log a [TODO] in PROGRESS_LOG. The active workflow agent implements it. Ownership is tracked via PROGRESS_LOG entries: [ACTIVE] workflow_owner: <agent> at session start, [DONE] workflow session complete when done. Per-firm customization is the SaaS admin's domain — bridge agents never customize per-tenant. When the template is production-ready, it will be frozen READ-ONLY for all bridge agents.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
