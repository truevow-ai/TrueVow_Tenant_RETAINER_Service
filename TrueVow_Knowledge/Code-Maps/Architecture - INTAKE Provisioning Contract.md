---
category: architecture
title: "INTAKE Provisioning Contract"
importance: 8
tags: []
file_paths: []
created: 2026-08-11T10:28:24.605871+00:00
updated: 2026-08-11T10:28:24.605871+00:00
memory_id: 781d8c85-9551-4613-9d16-d6237f705c16
---

# INTAKE Provisioning Contract

The canonical SaaS Admin -> INTAKE provisioning contract is at POST /api/v1/internal/tenants/provision (PLG-INTAKE-01). HMAC signing: timestamp:POST:{path}:body_hash using SAAS_ADMIN_WEBHOOK_SECRET. Replay window 300s. The /webhooks/saas-admin endpoint is a LIFECYCLE webhook only (subscription events) — not provisioning. Application plane separation: provisioning is cold-path REST API, separate from voice/audio hot path.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
