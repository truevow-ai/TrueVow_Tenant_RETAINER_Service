---
category: decision
title: "INTAKE\u2192RETAINER webhook live-tested against Supabase \u2014 8/8 pass"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T06:07:29.855208+00:00
updated: 2026-07-31T06:07:29.855208+00:00
memory_id: 402d248b-0760-4d38-91a0-9b40fb5fc3dc
---

# INTAKE→RETAINER webhook live-tested against Supabase — 8/8 pass

All live webhook tests pass against Supabase Pooler (cnbzuiuyppzrygxllgxj): valid primary key (202), unknown key (401), modified body (401), trailing slash (401), query string (401), missing headers (401), expired timestamp (401), secondary key rotation (202). HMAC WebhookSignature v1.0 verified end-to-end with real Supabase. Key fixes: case-insensitive headers, get_db_public for webhooks, TENANT_RETAINER_DATABASE_URL alias, SQLite removed.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
