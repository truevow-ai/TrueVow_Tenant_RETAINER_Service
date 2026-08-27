---
category: bug
title: "D3 UPGRADED TO SEVERITY 1: RETAINER per-service key isolation \u2014 authentication boundary failure"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T04:49:28.576845+00:00
updated: 2026-07-31T04:49:28.576845+00:00
memory_id: dde1dd8a-58a8-4dee-8c74-399d4a30aadb
---

# D3 UPGRADED TO SEVERITY 1: RETAINER per-service key isolation — authentication boundary failure

RETAINER webhook_signature.py:122-124 maps ALL per-service registry keys to same fallback secret. A compromised service could impersonate another. Required fix: remove every global-secret fallback; resolve explicit per-key records (key_id, secret, caller_service, receiver_service, allowed_method, allowed_path, env, enabled, valid_from, valid_until). tv-intake-to-retainer-v1 must ONLY authorize INTAKE→RETAINER POST /api/v1/retainer/webhooks/candidate-submitted — never activation or TRACE delivery. Owner: ghaus-fsd.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
