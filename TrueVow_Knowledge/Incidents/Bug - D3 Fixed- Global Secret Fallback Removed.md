---
category: bug
title: "D3 Fixed: Global Secret Fallback Removed"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T04:54:45.280328+00:00
updated: 2026-07-31T04:54:45.280328+00:00
memory_id: 4356220d-c77c-423e-a16d-3af7a742bcff
---

# D3 Fixed: Global Secret Fallback Removed

RETAINER webhook_signature.py: sign_request() no longer falls back to settings.service_api_key. _resolve_secret() no longer falls back to TRUEVOW_WEBHOOK_SECONDARY_KEYS universal pool. deps.py: legacy bearer validates against per-link keys only. Each key resolved strictly from WEBHOOK_KEY_<KEY_ID> env var. Severity 1 — authentication boundary failure.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
