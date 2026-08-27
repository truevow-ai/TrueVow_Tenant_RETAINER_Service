---
category: bug
title: "DELIVERY_MODE=disabled False Evidence"
importance: 8
tags: []
file_paths: []
created: 2026-08-10T15:53:38.231456+00:00
updated: 2026-08-10T15:53:38.231456+00:00
memory_id: 600762e2-3141-4115-b5af-a308949230f6
---

# DELIVERY_MODE=disabled False Evidence

ONBOARDING_EXTERNAL_DELIVERY_MODE=disabled does NOT hold commands. It marks them DELIVERED with http_status 200, advances steps to SUCCEEDED, triggers dependency release, and advances run lifecycle. Creates fabricated success evidence across 4 tables. Not safe as a pause/hold mechanism. SaaS Admin lib/services/durable-onboarding.ts:16 and cron route at app/api/cron/onboarding/process/route.ts:350-367.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
