---
category: decision
title: "TRACE Per-Link Webhook Key Isolation"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:41:54.643251+00:00
updated: 2026-07-31T03:41:54.643251+00:00
memory_id: a1735032-8258-443d-8b92-3e0a1416f0d4
---

# TRACE Per-Link Webhook Key Isolation

Webhook keys are now per-service-relationship, not global. TRACE uses tv-saas-admin-to-trace-v1 for incoming matter.activated from SaaS Admin. Same key must not be reused for INTAKE->RETAINER or RETAINER->SaaS Admin. Compromising one service must not enable impersonation of all others. Secondary rotation keys also per-link (tv-saas-admin-to-trace-v2). Documented in AGENTS.md implementation rules.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
