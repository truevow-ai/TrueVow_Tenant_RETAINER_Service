---
category: architecture
title: "Trial States"
importance: 9
tags: []
file_paths: []
created: 2026-08-10T18:29:35.214940+00:00
updated: 2026-08-10T18:29:35.214940+00:00
memory_id: d438e670-ab47-4751-aaae-d9e64164c812
---

# Trial States

Lifecycle states: APPROVED -> ONBOARDING -> TEST_CALL -> TRIAL_ACTIVATED (12 intakes/90 days). Customer may select PAID_PLAN_SCHEDULED at any time during trial. Trial remains authoritative until TRIAL_ENDED (first of: 12th intake or day 90). Then atomic transition to PAID_PLAN_ACTIVE with monthly allowance. No gap, no interruption.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
