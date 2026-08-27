---
category: decision
title: "Billing Trial Implementation \u2014 CONDITIONALLY APPROVED"
importance: 10
tags: []
file_paths: []
created: 2026-08-10T19:26:33.521343+00:00
updated: 2026-08-10T19:26:33.521343+00:00
memory_id: b0d8fc5c-8023-491d-af91-193b25bc88ae
---

# Billing Trial Implementation — CONDITIONALLY APPROVED

Commercial model APPROVED. 18 revisions required before implementation: 1) Keep TRIAL_ACTIVE after successor selection 2) Separate successor plan from current subscription status 3) Three timestamps: trial_expires_at/trial_ended_at/trial_end_reason 4) Versioned trial offer (INTAKE_TRIAL_90D_12_V1) 5) FK must point to immutable pricing catalogue 6) Freeze price at selection 7) Reuse canonical Billing usage ingestion 8) Register exact meterable INTAKE event 9) Idempotent intake counting 10) Immediate conversion on 12th intake not daily sweep 11) Atomic concurrency-safe transition 12) SaaS Admin triggers trial activation after readiness gate 13) SaaS Admin retains operational entitlement authority 14) Do not use renew_subscription for trial conversion 15) Explicit scheduled-plan command 16) Defer immediate_activation 17) Define no-successor TRIAL_EXPIRED behavior 18) Define billing-readiness before auto-conversion guarantee.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
