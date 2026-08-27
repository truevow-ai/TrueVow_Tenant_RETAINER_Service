---
category: pattern
title: "SaaS Admin: Migration Runner Pattern"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T02:55:35.927753+00:00
updated: 2026-07-31T02:55:35.927753+00:00
memory_id: bf32bbec-5cba-460c-9f00-7a57cc1ba8dd
---

# SaaS Admin: Migration Runner Pattern

Migrations must be applied to live DB, not just written as SQL files. Pattern: node scripts/_migrate_NNN_description.js. Uses pg Client with connectionString + ssl: { rejectUnauthorized: false }. Always IF NOT EXISTS guards. Audit triggers use audit_trigger_func_v2() with actor_type='automated_job', event_category='configuration'. Never use psql \set commands with pg client.

---
**Category:** `pattern` | **Importance:** 8/10
**Files:** N/A
