---
category: decision
title: "Billing architecture finalized \u2014 all three services updated"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T20:24:15.794219+00:00
updated: 2026-07-31T20:24:15.794219+00:00
memory_id: fe49f288-2472-431c-ab45-00c399263253
---

# Billing architecture finalized — all three services updated

Billing Service constants.py: full spec including usage meters (INTAKE calls not minutes, TRACE per-matter, SETTLE reports, COMMAND subscription), subscription states, entitlement gates per tier, billing-to-accounting contract, upgrade/downgrade rules, first 12 TRACE credits. Customer Portal pricing-snapshot.json rewritten with current model. Financial Accounting schemas clarified as Billing-dependent. RETAINER is internal service packaged inside TRACE. Public suite: INTAKE (// call-based), TRACE (// per matter), SETTLE (/), COMMAND (Core free, Pro ).

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
