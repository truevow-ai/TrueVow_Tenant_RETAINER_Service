---
category: architecture
title: "INTAKE Provisioning Endpoint Found"
importance: 9
tags: []
file_paths: []
created: 2026-08-11T04:38:19.600249+00:00
updated: 2026-08-11T04:38:19.600249+00:00
memory_id: 15cb63cd-006f-4119-a2ce-03198b98aa70
---

# INTAKE Provisioning Endpoint Found

INTAKE already has canonical provisioning endpoint at POST /api/v1/internal/tenants/provision on truevow-tenant-public. Uses HMAC-SHA256 with timestamp replay guard. Also has /api/v1/internal/tenants/activate. SaaS Admin provision_tenant handler incorrectly targets /webhooks/saas-admin. Fix: update handler URL to /api/v1/internal/tenants/provision with correct HMAC signing format.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
