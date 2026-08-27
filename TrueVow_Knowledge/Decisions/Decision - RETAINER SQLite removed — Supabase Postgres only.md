---
category: decision
title: "RETAINER SQLite removed \u2014 Supabase Postgres only"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T06:04:14.472536+00:00
updated: 2026-07-31T06:04:14.472536+00:00
memory_id: 3db87a34-f89c-4748-9122-52a4c0aa70cd
---

# RETAINER SQLite removed — Supabase Postgres only

SQLite fallback removed from RETAINER config.py, database.py, and main.py. effective_database_url now raises RuntimeError if no Supabase URL configured. This is a platform rule: all services communicate only with Supabase. No SQLite substitutes accepted as evidence in any QA or staging test. Commits: 8ab03dd (remove SQLite) + 1e91875 (add TENANT_RETAINER_DATABASE_URL alias).

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
