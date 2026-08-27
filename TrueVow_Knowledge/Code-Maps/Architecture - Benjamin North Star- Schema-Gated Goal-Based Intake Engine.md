---
category: architecture
title: "Benjamin North Star: Schema-Gated Goal-Based Intake Engine"
importance: 10
tags: []
file_paths: []
created: 2026-08-12T17:51:38.905602+00:00
updated: 2026-08-12T17:51:38.905602+00:00
memory_id: 755c7343-49ce-4447-8ff5-cf9c3ae3af1e
---

# Benjamin North Star: Schema-Gated Goal-Based Intake Engine

CTO research decision: evolve Benjamin from FSM+QuestionRunner to schema-guided goal-based architecture. Firms configure FACTS (incident.location, injury.present) + GOALS + POLICY branches — NOT questions or node graphs. One caller sentence extracts multiple candidate facts, validated separately. Lifecycle shrinks to ~6 states (BOOTSTRAP/SCREENING/INTAKE/RESOLUTION/AWAITING_EFFECT/COMPLETE + HANDOFF/TERMINATED). LLM = conversation conductor within code-determined agenda; code = agenda authority. LiveKit = voice runtime only, TrueVow Core consumes provider-neutral CoreTurn. First Call Readiness Certificate requires all policy branches have outcomes + effect fallbacks; external integrations NOT required for first call. Prototype-first: challenger (Car Accident + OPI) vs current 22-state FSM, measure task completion/false commits/repeats/turns. SaaS Admin Builder implication: NOT a flowchart editor — firm configures facts, routing policy, destinations; previews generated sample conversations.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
