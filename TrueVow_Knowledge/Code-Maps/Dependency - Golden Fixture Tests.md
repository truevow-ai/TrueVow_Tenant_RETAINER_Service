---
category: dependency
title: "Golden Fixture Tests"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T03:42:31.996752+00:00
updated: 2026-07-31T03:42:31.996752+00:00
memory_id: 185b2959-eeda-4401-8e64-f2f39449e9ca
---

# Golden Fixture Tests

tests/security/webhook-signature.test.ts has 16 golden fixture tests that must pass identically in TypeScript and Python. Covers: golden verify, deterministic HMAC, sign+verify roundtrip, expired, future, tampered, wrong path, trailing slash, reserialized JSON, missing headers, non-numeric timestamp, wrong method, unknown key-id, internal consistency. Committed as source commit a18dae1.

---
**Category:** `dependency` | **Importance:** 9/10
**Files:** N/A
