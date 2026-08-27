---
category: bug
title: "D4 FIXED: INTAKE golden fixture tests augmented (23/23 pass)"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T05:18:22.945940+00:00
updated: 2026-07-31T05:18:22.945940+00:00
memory_id: 288061e0-2ebb-4769-ba3d-0b8719fa865f
---

# D4 FIXED: INTAKE golden fixture tests augmented (23/23 pass)

INTAKE test_webhook_signature_contract.py already existed with 14 tests. Added 9 new tests: query string rejection, encoded path rejection, double-slash rejection, non-ASCII raw body, deterministic signature, secondary key verification, secondary key gating, exact canonical path, timestamp precision warning. Fixed at commit 8c6ec5c.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
