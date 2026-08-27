---
category: decision
title: "All DB insert paths now gated server-side (full audit)"
importance: 10
tags: []
file_paths: []
created: 2026-07-11T03:23:08.221057+00:00
updated: 2026-07-11T03:23:08.221057+00:00
memory_id: e999e643-e35b-45f5-88f5-e4a2609c4335
---

# All DB insert paths now gated server-side (full audit)

Fiduciary audit of every settle_verdicts/settle_contributions insert repo-wide. Gaps found+closed: (1) API bulk_insert_verdicts + create_verdict had NO gate -> added app/services/verdict_guard.py (provenance+verbatim-evidence+enum+bounds, strips unverifiable fields, rejects no-provenance); (2) seed_test_data.py fabricates random.uniform() rows -> blocked unless localhost+SETTLE_ALLOW_TEST_SEED; (3) archived 37 ungated scrapers/feeders. contributor.py is legit (firm submission, blockchain_hash, consent, DataValidator+anomaly). CI guard 15 tests / 4 layers. Only gated paths remain: cds loaders, load_direct_supabase, API (guarded), contributor (attested).

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
