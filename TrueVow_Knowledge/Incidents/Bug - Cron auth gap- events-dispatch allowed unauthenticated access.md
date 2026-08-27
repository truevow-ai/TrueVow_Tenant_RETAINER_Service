---
category: bug
title: "Cron auth gap: events/dispatch allowed unauthenticated access"
importance: 8
tags: []
file_paths: []
created: 2026-08-11T10:28:26.758915+00:00
updated: 2026-08-11T10:28:26.758915+00:00
memory_id: 77b44ea4-713c-4ce4-a50d-b6dbe1f0072d
---

# Cron auth gap: events/dispatch allowed unauthenticated access

events/dispatch/route.ts used if(cronSecret && authHeader !== ...) which allowed unauthenticated access when CRON_SECRET was unset. Fixed to use if(!CRON_SECRET || token !== CRON_SECRET) pattern matching all other cron routes.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
