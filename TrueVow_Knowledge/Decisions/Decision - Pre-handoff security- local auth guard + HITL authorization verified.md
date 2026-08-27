---
category: decision
title: "Pre-handoff security: local auth guard + HITL authorization verified"
importance: 9
tags: []
file_paths: []
created: 2026-08-03T23:00:52.344263+00:00
updated: 2026-08-03T23:00:52.344263+00:00
memory_id: b1f7a643-ad5f-4b7b-a249-5a85c06f441c
---

# Pre-handoff security: local auth guard + HITL authorization verified

lib/auth.ts: local dev UUID blocked in production/staging (NODE_ENV guard). Added requireInternalRole() - rejects tenant users. HITL route now uses requireInternalRole() instead of bare requireAuth(). Audit records actual actor (not assignedTo). SUPABASE_SERVICE_ROLE_KEY server-side only - no NEXT_PUBLIC_ prefix. 660 TS + 17 Python = 677 passed, 0 failed.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
