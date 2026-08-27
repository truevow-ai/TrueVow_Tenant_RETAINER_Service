---
category: decision
title: "SaaS Admin /tenants/internal REJECTED"
importance: 9
tags: []
file_paths: []
created: 2026-08-10T15:42:38.088333+00:00
updated: 2026-08-10T15:42:38.088333+00:00
memory_id: 0a15f74a-fb3b-4379-9c05-89479e6008df
---

# SaaS Admin /tenants/internal REJECTED

POST /api/v1/tenants/internal was proposed by SaaS Admin agent but REJECTED as canonical architecture. CSM must not directly create tenants. The canonical flow is: Sales Ops -> SaaS Admin -> CSM. SaaS Admin owns authoritative commissioning.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
