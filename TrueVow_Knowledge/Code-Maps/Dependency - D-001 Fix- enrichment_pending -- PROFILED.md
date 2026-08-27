---
category: dependency
title: "D-001 Fix: enrichment_pending -> PROFILED"
importance: 8
tags: []
file_paths: []
created: 2026-08-03T19:36:22.843816+00:00
updated: 2026-08-03T19:36:22.843816+00:00
memory_id: fb4066e9-a3c2-46d7-b034-c38374f2e0db
---

# D-001 Fix: enrichment_pending -> PROFILED

enrichment_pending maps to canonical PROFILED per CTO frozen decision. Next valid transition: T004 (PROFILED -> CONTACT_ENRICHED). Reason code: legacy_state_migrated. Fixed in contracts.ts, migration 177, website-intake/manager.ts, and leads-repository.ts.

---
**Category:** `dependency` | **Importance:** 8/10
**Files:** N/A
