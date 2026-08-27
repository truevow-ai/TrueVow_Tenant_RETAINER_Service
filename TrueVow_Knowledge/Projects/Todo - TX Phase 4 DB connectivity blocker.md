---
category: todo
title: "TX Phase 4 DB connectivity blocker"
importance: 10
tags: []
file_paths: []
created: 2026-07-27T17:55:15.974217+00:00
updated: 2026-07-27T17:55:15.974217+00:00
memory_id: db240cad-fa85-45d8-aa36-6ae76d5aee81
---

# TX Phase 4 DB connectivity blocker

db.bpzegquhxnygyxdzluyw.supabase.co only resolves to IPv6, Windows dev box has no IPv6. Supabase pooler not enabled for this project (tenant/user not found). Phase 4 scripts (verify_emails_phones, classify_phone_types, verify_attorney_emails) need psycopg2. Workaround: create REST API versions or enable IPv4 on Supabase.

---
**Category:** `todo` | **Importance:** 10/10
**Files:** N/A
