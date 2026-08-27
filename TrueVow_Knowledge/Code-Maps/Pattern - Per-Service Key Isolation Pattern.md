---
category: pattern
title: "Per-Service Key Isolation Pattern"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:41:21.252618+00:00
updated: 2026-07-31T03:41:21.252618+00:00
memory_id: 0745c2aa-00a0-4a9d-b60c-6b58998147a8
---

# Per-Service Key Isolation Pattern

NEVER use one global webhook secret across all services. Each caller-receiver pair gets its own key: tv-intake-to-retainer-v1, tv-retainer-to-saas-admin-v1, tv-saas-admin-to-trace-v1. Key prefixes bound to allowed paths in CANONICAL_PATHS registry. Env vars: TRUEVOW_WEBHOOK_KEY_ID_{SERVICE} + TRUEVOW_WEBHOOK_SECRET_{SERVICE}. Secondary rotation keys per-relationship, not universal. Compromising one service must not allow impersonation of others.

---
**Category:** `pattern` | **Importance:** 10/10
**Files:** N/A
