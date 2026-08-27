---
category: architecture
title: "Per-Link Key Isolation"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:41:38.631261+00:00
updated: 2026-07-31T03:41:38.631261+00:00
memory_id: 791dbdb7-490b-4530-a7aa-f7904f63f059
---

# Per-Link Key Isolation

Replaced global TRUEVOW_WEBHOOK_SECRET with per-link key pairs: tv-intake-to-retainer-v1, tv-retainer-to-saas-admin-v1, tv-saas-admin-to-trace-v1. Each key binds to specific caller, receiver, path, and method. A key valid for one link MUST NOT be accepted on another. verifySignature() validates key binding in addition to HMAC. Rotation keys also per-link, not universal.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
