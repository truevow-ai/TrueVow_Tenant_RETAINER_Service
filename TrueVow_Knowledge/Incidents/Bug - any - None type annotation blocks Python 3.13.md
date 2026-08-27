---
category: bug
title: "any | None type annotation blocks Python 3.13"
importance: 8
tags: []
file_paths: []
created: 2026-07-26T23:19:34.746311+00:00
updated: 2026-07-26T23:19:34.746311+00:00
memory_id: 45269e5b-2df9-4671-a52d-4e0c74053d54
---

# any | None type annotation blocks Python 3.13

database.py used lowercase 'any' instead of 'Any' from typing. Python 3.13 correctly rejects this since 'any' is a builtin function, not a type. Fixed by importing Any and correcting annotations.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
