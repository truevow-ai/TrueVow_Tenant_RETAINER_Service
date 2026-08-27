---
category: architecture
title: "Schema-Gated Intake Engine \u2014 North Star"
importance: 10
tags: []
file_paths: []
created: 2026-08-12T17:51:19.244717+00:00
updated: 2026-08-12T17:51:19.244717+00:00
memory_id: b7d714b4-ef3b-4bc7-a5d6-cf10e2376398
---

# Schema-Gated Intake Engine — North Star

Benjamin final architecture direction: schema-guided, goal-based, mixed-initiative legal intake with deterministic policy and execution gates. Talk naturally, collect against a schema, decide against deterministic policy, execute only through validated effects. Lifecycle shrinks to ~8 states (BOOTSTRAP, SCREENING, INTAKE, RESOLUTION, AWAITING_EFFECT, COMPLETE + HANDOFF, TERMINATED). Facts+goals replace questions+states. LLM chooses how to converse within permitted agenda; code determines agenda. LiveKit becomes voice runtime only, not second orchestration framework. One caller sentence can satisfy multiple fact requirements — never re-ask.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
