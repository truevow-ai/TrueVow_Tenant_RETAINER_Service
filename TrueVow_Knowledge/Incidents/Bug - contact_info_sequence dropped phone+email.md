---
category: bug
title: "contact_info_sequence dropped phone+email"
importance: 9
tags: []
file_paths: []
created: 2026-07-14T10:50:56.673190+00:00
updated: 2026-07-14T10:50:56.673190+00:00
memory_id: 6c880177-8100-461d-a2bb-57440370463c
---

# contact_info_sequence dropped phone+email

Root cause: routing INTO a sequence node used _execute_node, which returned the sequence's own intro prompt and left current_node=contact_info_sequence WITHOUT priming the first sub-node. Next turn the C10 terminal guard (workflow_engine.py:518) saw no next/branches/options and returned _build_complete_response — so name-only leads jumped to 'complete', losing phone+email. FIX: _execute_node now delegates type==sequence to _execute_sequence (primes contact_name, prepends intro to first question); terminal guards treat nodes/type==sequence as a valid exit. Verified: name->phone->email chain now runs.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
