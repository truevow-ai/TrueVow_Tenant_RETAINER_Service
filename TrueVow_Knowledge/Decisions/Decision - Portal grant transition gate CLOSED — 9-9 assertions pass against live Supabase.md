---
category: decision
title: "Portal grant transition gate CLOSED \u2014 9/9 assertions pass against live Supabase"
importance: 10
tags: []
file_paths: []
created: 2026-08-01T01:33:57.786365+00:00
updated: 2026-08-01T01:33:57.786365+00:00
memory_id: 1039ea34-0802-4396-b7af-502716507d36
---

# Portal grant transition gate CLOSED — 9/9 assertions pass against live Supabase

PROSPECTIVE_ENGAGEMENT -> READ_ONLY_HISTORY + ACTIVE_MATTER with MATTER_VIEW/MATTER_MESSAGE/MATTER_UPLOAD/REQUEST_RESPOND/DOCUMENT_DOWNLOAD verified. Shared Platform owns MATTER_* permissions. RETAINER keeps ENGAGEMENT_HISTORY only. TRACE consumes tenant-scoped projection linked to canonical grant. Identity continuity, duplicate/orphan prevention, fail-safe missing-grant behavior all proven. Commit: 56720be. Customer pilot now blocked by 5 remaining gates: live activation HTTP, durable outbox traceability, stable staging deployment, Client Portal browser lifecycle, remaining QA phases.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
