---
category: decision
title: "G11 Worker Fix: Removed .env.staging dependency"
importance: 8
tags: []
file_paths: []
created: 2026-08-11T10:28:26.250053+00:00
updated: 2026-08-11T10:28:26.250053+00:00
memory_id: 1210f6c9-e2c5-4aa1-9167-17df0431a29a
---

# G11 Worker Fix: Removed .env.staging dependency

SaaS Admin onboarding-command-worker.js now uses pg Pool with SAAS_ADMIN_DATABASE_SESSION_POOLER_URL || SAAS_ADMIN_DATABASE_URL || DATABASE_URL, matching durable-onboarding.ts pattern. Template literal SQL intervals replaced with parameterized queries. Pool connection verified on startup before polling loop.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
