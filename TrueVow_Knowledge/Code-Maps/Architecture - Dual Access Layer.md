---
category: architecture
title: "Dual Access Layer"
importance: 8
tags: []
file_paths: []
created: 2026-08-10T15:43:18.145175+00:00
updated: 2026-08-10T15:43:18.145175+00:00
memory_id: bf3feb35-98b2-4a55-8d48-80700d68e0e3
---

# Dual Access Layer

Sales Ops has two data layers: pg Pool (direct PG via PG_DATABASE_URL) used by dashboard and API routes, and supabaseAdmin (Supabase JS client) used by repositories/transitions. These do NOT talk to each other. supabaseAdmin is IP-restricted. Migration for new columns needed on both paths.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
