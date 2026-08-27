---
category: bug
title: "D3 ALREADY FIXED: RETAINER per-service key isolation at commit 05ee2e3"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T05:18:21.519561+00:00
updated: 2026-07-31T05:18:21.519561+00:00
memory_id: 350dc9f8-ed92-4a98-b89f-dd32c09bd0e3
---

# D3 ALREADY FIXED: RETAINER per-service key isolation at commit 05ee2e3

RETAINER webhook_signature.py _resolve_secret already uses per-key env vars (WEBHOOK_KEY_<KEY_ID>) with no global fallback. sign_request() requires explicit secret. verify_signature() enforces PATH_NOT_ALLOWED and METHOD_NOT_ALLOWED per key. D3 was fixed before the QA scan — QA agent tested against an older SHA.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
