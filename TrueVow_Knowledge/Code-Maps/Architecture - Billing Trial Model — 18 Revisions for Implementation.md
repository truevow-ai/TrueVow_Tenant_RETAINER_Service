---
category: architecture
title: "Billing Trial Model \u2014 18 Revisions for Implementation"
importance: 9
tags: []
file_paths: []
created: 2026-08-10T19:25:27.089175+00:00
updated: 2026-08-10T19:25:27.089175+00:00
memory_id: 2b7ca583-e39a-4ca0-a30d-3e927f920604
---

# Billing Trial Model — 18 Revisions for Implementation

Trial lifecycle separated into 3 timestamps: trial_started_at, trial_expires_at (deterministic 90-day deadline), trial_ended_at (actual). TRIAL_ACTIVE persists after plan selection — successor_plan is a separate field, not a subscription status transition. Trial→paid must be atomic (no TRIAL_ENDED window, no gap). Usage counting must be idempotent by intake_session_id via existing INTAKE→Billing pipeline. Intake limit conversion must happen immediately on 12th event, not via daily sweeper. SaaS Admin triggers trial activation only after readiness gate (not after onboarding form). SaaS Admin retains operational entitlement authority — Billing owns commercial fact only. Defer immediate_activation. Defer upgrade overloading. Trial offer is versioned (INTAKE_TRIAL_90D_12_V1) with immutable terms.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
