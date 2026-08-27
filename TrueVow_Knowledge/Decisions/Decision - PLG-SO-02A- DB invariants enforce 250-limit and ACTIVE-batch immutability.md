---
category: decision
title: "PLG-SO-02A: DB invariants enforce 250-limit and ACTIVE-batch immutability"
importance: 9
tags: []
file_paths: []
created: 2026-08-03T21:15:23.012216+00:00
updated: 2026-08-03T21:15:23.012216+00:00
memory_id: 462d8f57-0246-4656-8703-ac0995386104
---

# PLG-SO-02A: DB invariants enforce 250-limit and ACTIVE-batch immutability

Migration 182 adds: trg_batch_member_limit (advisory lock, 250-max), trg_prevent_active_batch_mutation (12 immutable fields), trg_prevent_member_delete (membership freeze), governed_remove_batch_member() (soft-delete), v_batch_size_mismatches (0 rows expected). Full regression: 563 TS + 17 Python. PLG suites: 139/139 PASS.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
