---
category: bug
title: "D1 FIXED: SaaS Admin test env vars aligned (22/22 pass)"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T05:18:18.273628+00:00
updated: 2026-07-31T05:18:18.273628+00:00
memory_id: 60ff76a2-5ad9-4efa-8e3d-918fe704f049
---

# D1 FIXED: SaaS Admin test env vars aligned (22/22 pass)

SaaS Admin webhook-signature.test.ts beforeAll was using old env var names (TRUEVOW_WEBHOOK_KEY_ID/SECRET) instead of per-relationship names (TRUEVOW_WEBHOOK_KEY_ID_RETAINER/SECRET_RETAINER). Fixed at commit 2e95a5e. All 22 golden fixture tests pass including trailing-slash, query-string, encoded-path, double-slash rejection.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
