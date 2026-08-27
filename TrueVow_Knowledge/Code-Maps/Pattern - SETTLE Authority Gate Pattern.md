---
category: pattern
title: "SETTLE Authority Gate Pattern"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T02:56:33.728350+00:00
updated: 2026-07-31T02:56:33.728350+00:00
memory_id: bdd62b4a-0cdd-42b7-a3b2-64ff93aaec08
---

# SETTLE Authority Gate Pattern

Every material action in SETTLE passes through a three-layer gate: (1) Authority class check - who can do what (CLIENT_AUTH for settlement decisions, ATTY_AUTH for demand/representation, STAFF_AUTH for disbursements). (2) State transition validation - is this move allowed from the current state (6 transition maps: demand_package, offer, lien, allocation, disbursement, consent). (3) Invariant validation - does this action violate any non-negotiable rule (INV-005 client settlement authority, INV-013 money reconciliation, INV-006 immutable document versions). Failure mode is always fail-closed (TV-CMP-002).

---
**Category:** `pattern` | **Importance:** 8/10
**Files:** N/A
