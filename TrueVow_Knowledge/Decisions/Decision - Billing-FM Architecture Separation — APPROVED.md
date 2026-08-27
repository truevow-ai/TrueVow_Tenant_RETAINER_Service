---
category: decision
title: "Billing-FM Architecture Separation \u2014 APPROVED"
importance: 10
tags: []
file_paths: []
created: 2026-08-04T03:17:48.649593+00:00
updated: 2026-08-04T03:17:48.649593+00:00
memory_id: d95cc74d-35de-4471-b0ad-591fc31489a5
---

# Billing-FM Architecture Separation — APPROVED

Tenant Billing becomes a pure commercial subscription, metering and rating engine. Financial Management owns customer invoices, AR, payment execution, allocations, refunds, collections, treasury reconciliation and accounting. One contract connects them: CommercialStatementFinalized. Billing produces immutable commercial statements with line items; FM converts them into posted invoices, AR entries, and journal postings. Billing must NOT own: invoices, payments, payment providers, refunds, allocations, collections. FM must NOT recalculate pricing, usage, allowances or discounts. The fact that Billing is currently described as production-ready is not a valid reason to retain the wrong boundary. Full decision doc at TrueVow_Financial_Management_Service/docs/BILLING_FM_ARCHITECTURE_DECISION.md

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
