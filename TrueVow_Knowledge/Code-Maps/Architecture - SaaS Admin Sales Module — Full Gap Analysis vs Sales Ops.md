---
category: architecture
title: "SaaS Admin Sales Module \u2014 Full Gap Analysis vs Sales Ops"
importance: 10
tags: []
file_paths: []
created: 2026-07-24T10:36:35.075089+00:00
updated: 2026-07-24T10:36:35.075089+00:00
memory_id: beba7fa4-e29a-4513-af7b-78e1fa8eb857
---

# SaaS Admin Sales Module — Full Gap Analysis vs Sales Ops

Audit found ZERO integration between SaaS Admin and Sales Ops. SaaS Admin has its own Sales CRM Service (separate microservice for B2B SaaS sales pipeline) with 34 proxy routes. Key findings: (1) Sales homepage is a stub with MOCK_SALES_LEADS — no API calls. (2) Two no-op webhook handlers (tenant-status-changed, subscription-updated). (3) Broken provisioning/onboarding/qualification pages depending on missing /api/v1/tenants. (4) Two contact tables (core_contacts + customer_contacts) — no single source of truth. (5) No SALES_OPS_URL env var, no Sales Ops API client, no webhook receiver for application-approved events. (6) No 'convert to tenant' path from Sales Ops pipeline. (7) Archived sales tables from migration 079 may still exist as bloat. Full gap analysis written to docs/SALES_OPS_GAP_ANALYSIS.md with 5-phase action plan.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
