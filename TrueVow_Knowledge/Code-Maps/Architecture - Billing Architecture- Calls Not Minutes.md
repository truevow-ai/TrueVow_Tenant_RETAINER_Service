---
category: architecture
title: "Billing Architecture: Calls Not Minutes"
importance: 8
tags: []
file_paths: []
created: 2026-08-01T03:49:16.090911+00:00
updated: 2026-08-01T03:49:16.090911+00:00
memory_id: 09348c09-0588-4b33-a899-bced888d5734
---

# Billing Architecture: Calls Not Minutes

INTAKE customer pricing is per billable call (Solo: 40/5, Growth: 100/2, Team: 200/0). Duration is internal cost metric only. Product services emit usage events; Billing rates and controls entitlements; Financial Accounting creates invoices; Customer Portal displays plans/usage/invoices. INTAKE emits intake.call.completed events with session_id, duration_seconds, highest_intake_state, billing_qualification_hint. Four-layer entitlement gates. Subscription states: PENDING/TRIAL/ACTIVE/PAST_DUE/GRACE/SUSPENDED/CANCELLED/EXPIRED. Fail-closed for new commercial commitments, preserve legal records access.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
