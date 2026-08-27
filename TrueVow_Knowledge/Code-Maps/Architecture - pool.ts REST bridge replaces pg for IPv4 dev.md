---
category: architecture
title: "pool.ts REST bridge replaces pg for IPv4 dev"
importance: 8
tags: []
file_paths: []
created: 2026-08-11T02:06:18.972203+00:00
updated: 2026-08-11T02:06:18.972203+00:00
memory_id: 59ceced9-c6fd-4701-a30a-261c5e2e4582
---

# pool.ts REST bridge replaces pg for IPv4 dev

lib/db/pool.ts rewritten to use Supabase JS client (REST API) instead of direct pg Pool, enabling IPv4-only Windows development. Translates basic SQL (SELECT/UPDATE/INSERT/DELETE) to Supabase API calls. Converts camelCase responses back to snake_case. Handles COUNT(*), ILIKE, OR conditions, OFFSET/LIMIT pagination.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
