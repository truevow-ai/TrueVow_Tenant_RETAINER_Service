---
category: bug
title: "D3: RETAINER per-service key isolation not enforced (Severity 2)"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T04:40:16.812483+00:00
updated: 2026-07-31T04:40:16.812483+00:00
memory_id: 0ee7c415-77c8-405b-ac3a-93c6f29851fb
---

# D3: RETAINER per-service key isolation not enforced (Severity 2)

RETAINER webhook_signature.py:122-124 maps ALL per-service registry keys to same fallback secret. tv-intake-to-retainer-v1 and tv-retainer-to-saas-admin-v1 share credentials in default code path. Owner: ghaus-fsd.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
