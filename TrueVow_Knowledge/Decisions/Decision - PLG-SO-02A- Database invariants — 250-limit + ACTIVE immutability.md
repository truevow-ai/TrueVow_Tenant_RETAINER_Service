---
category: decision
title: "PLG-SO-02A: Database invariants \u2014 250-limit + ACTIVE immutability"
importance: 9
tags: []
file_paths: []
created: 2026-08-05T07:37:36.650027+00:00
updated: 2026-08-05T07:37:36.650027+00:00
memory_id: 176f9702-7b56-423a-84c9-e90ad0cce39f
---

# PLG-SO-02A: Database invariants — 250-limit + ACTIVE immutability

Migration 182 adds: trg_batch_member_limit (pg_advisory_xact_lock per batch, 250-max), trg_prevent_active_batch_mutation (12 immutable fields), trg_prevent_member_delete (membership freeze), governed_remove_batch_member() (soft-delete), v_batch_size_mismatches (expected 0 rows). Concurrent final-slot insertion: exactly one succeeds.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
