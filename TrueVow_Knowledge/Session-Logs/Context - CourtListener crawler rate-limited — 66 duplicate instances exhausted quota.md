---
category: context
title: "CourtListener crawler rate-limited \u2014 66 duplicate instances exhausted quota"
importance: 6
tags: []
file_paths: []
created: 2026-07-08T08:50:04.051989+00:00
updated: 2026-07-08T08:50:04.051989+00:00
memory_id: 7042c842-e4a4-43e3-83bf-9ec63e5a7b40
---

# CourtListener crawler rate-limited — 66 duplicate instances exhausted quota

Root cause: supervisor Match pattern referenced cl_crawl which never appears in python.exe command line, so supervisor never detected the running crawler, launching a new one every 180s. 66 instances accumulated, collectively exhausting CourtListener's 125 req/day quota. Fixed: Match pattern simplified to just cds_courtlistener_crawl.py. Added per-URL failure counter (max 3) so crawler skips dead URLs. Crawler now waiting for daily rate limit reset.

---
**Category:** `context` | **Importance:** 6/10
**Files:** N/A
