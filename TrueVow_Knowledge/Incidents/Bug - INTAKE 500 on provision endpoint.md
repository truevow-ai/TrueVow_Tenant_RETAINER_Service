---
category: bug
title: "INTAKE 500 on provision endpoint"
importance: 8
tags: []
file_paths: []
created: 2026-08-11T09:38:38.385374+00:00
updated: 2026-08-11T09:38:38.385374+00:00
memory_id: e2f3b69d-5dd5-41a6-a174-a7fe858a0678
---

# INTAKE 500 on provision endpoint

INTAKE POST /api/v1/internal/tenants/provision returns 500 with empty body after HMAC auth passes. JSON validation works (400 on bad body). Template lookup or DB session fails internally — no middleware log entry for the request, suggesting exception before response handler. Tables exist, templates seeded, DB connected per health check. Likely: SQLAlchemy model-table schema mismatch, or get_db_session_context() async engine issue on Fly. Needs INTAKE agent to debug Fly logs.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
