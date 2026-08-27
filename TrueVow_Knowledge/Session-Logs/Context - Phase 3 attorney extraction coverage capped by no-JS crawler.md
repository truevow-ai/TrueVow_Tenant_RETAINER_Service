---
category: context
title: "Phase 3 attorney extraction coverage capped by no-JS crawler"
importance: 6
tags: []
file_paths: []
created: 2026-07-08T06:42:22.140637+00:00
updated: 2026-07-08T06:42:22.140637+00:00
memory_id: 7260ae78-f606-4eb1-8922-1306ecbd0363
---

# Phase 3 attorney extraction coverage capped by no-JS crawler

attorney_enrich.py uses plain aiohttp (no JS render). 759 FL firms with websites still yield empty attorneys because sites are JS-rendered SPAs. Coverage 58% of web-firms (1046/1805), 2793 total attorneys. To hit >90% target, upgrade Phase 3 to Playwright like Phase 2. CA firms cannot run Phase 3+ until loaded into Supabase (blocked on DB restore, direct Postgres 5432 permission denied; REST 443 works).

---
**Category:** `context` | **Importance:** 6/10
**Files:** N/A
