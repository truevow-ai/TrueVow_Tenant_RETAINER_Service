---
category: bug
title: "sales_handoff_outbox updated_at column"
importance: 8
tags: []
file_paths: []
created: 2026-08-10T15:42:46.665120+00:00
updated: 2026-08-10T15:42:46.665120+00:00
memory_id: b943289f-8419-4e89-b0de-49d0fc4f636e
---

# sales_handoff_outbox updated_at column

The sales_handoff_outbox table has no updated_at column. All UPDATE queries on this table must not reference updated_at. Fixed in both handoff-to-saas-admin and approve routes.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
