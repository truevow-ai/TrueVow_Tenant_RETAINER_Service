---
category: decision
title: "DELIVERY_MODE disabled fix + per-command eligibility gate deployed"
importance: 8
tags: []
file_paths: []
created: 2026-08-11T02:07:21.447494+00:00
updated: 2026-08-11T02:07:21.447494+00:00
memory_id: 5cc21ed0-71e9-4754-8e25-93096a9b1fe8
---

# DELIVERY_MODE disabled fix + per-command eligibility gate deployed

Three files changed: cron route, worker script, durable-onboarding docs. disabled mode now truly skips without state mutation. New ONBOARDING_ELIGIBLE_COMMANDS env var enables per-command dispatch gating. For G11/G11A controlled release: set ONBOARDING_ELIGIBLE_COMMANDS=provision_tenant,register_commercial_intent and DELIVERY_MODE=sandbox. ASSIGN_CSM and SEND_WELCOME_COMMUNICATION remain held as PENDING. No new state enum added — pure dispatcher filtering.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
