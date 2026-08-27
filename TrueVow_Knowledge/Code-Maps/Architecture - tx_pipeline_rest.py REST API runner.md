---
category: architecture
title: "tx_pipeline_rest.py REST API runner"
importance: 8
tags: []
file_paths: []
created: 2026-07-27T17:55:02.934642+00:00
updated: 2026-07-27T17:55:02.934642+00:00
memory_id: 22e3026c-0608-4d8c-9c1a-1a9a8f1b6d41
---

# tx_pipeline_rest.py REST API runner

Created scripts/tx_pipeline_rest.py — full pipeline runner using Supabase REST API only. Handles Phase 3 (flatten attorneys), Phase 7a (community tagging), Phase 7b (firm segregation), Phase 8 (attorney cohort segregation). Uses raw HTTP and supabase client for inserts. Avoids psycopg2/asyncpg dependency.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
