---
category: decision
title: "Per-Service Key Isolation \u2014 No Global Shared Secret"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:41:48.393437+00:00
updated: 2026-07-31T03:41:48.393437+00:00
memory_id: 28b9eab1-bd47-4fd1-8d86-0b5f278a4599
---

# Per-Service Key Isolation — No Global Shared Secret

Production must use caller-specific key IDs (tv-intake-to-retainer-v1, tv-retainer-to-saas-admin-v1), not one global tv-primary. Each receiver binds key to calling_service + allowed_paths + allowed_methods. Compromising one service must not enable impersonation of others. RETAINER _PER_SERVICE_KEY_REGISTRY enforces this.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
