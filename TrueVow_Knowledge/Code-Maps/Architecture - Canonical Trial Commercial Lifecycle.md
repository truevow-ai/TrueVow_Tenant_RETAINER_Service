---
category: architecture
title: "Canonical Trial Commercial Lifecycle"
importance: 9
tags: []
file_paths: []
created: 2026-08-10T18:30:59.861737+00:00
updated: 2026-08-10T18:30:59.861737+00:00
memory_id: 21f3a8dd-7c83-4c08-b294-f5cb84db6269
---

# Canonical Trial Commercial Lifecycle

Trial model: 90 days OR 12 completed intake sessions, whichever first. Three distinct phases: TRIAL_ACTIVE (authoritative entitlement), PAID_PLAN_SCHEDULED (customer committed but trial continues unchanged), PAID_PLAN_ACTIVE (trial exhausted/expired → paid activates atomically, no gap). Key distinction: plan_selected_at ≠ trial_ends_at ≠ paid_subscription_activated_at. 'Intake' defined as completed Benjamin session, not raw inbound call. Default path is scheduled conversion; immediate activation is optional with explicit confirmation (surrenders remaining trial). No payment on application page. Trial continues even after plan selection - customer is not punished for buying early.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
