---
category: architecture
title: "vNext Component Disposition"
importance: 9
tags: []
file_paths: []
created: 2026-08-12T17:51:56.833383+00:00
updated: 2026-08-12T17:51:56.833383+00:00
memory_id: 19b478f8-69a8-4faa-a787-29dd153a5f1a
---

# vNext Component Disposition

KEEP: compiler/checksum/versioning, tenant/config resolution, provider-neutral contracts, CandidateValidator, EffectRequest/EffectResult, effect idempotency, provider factories, fact schemas/catalogue. SHRINK: 22-state LifecycleFSM → ~8 states; custom Bridge orchestration substantially. EVOLVE: QuestionRunner → Goal/Agenda Engine; prompts → conversation hints. RETIRE: 133-node engine after proof. Not a rewrite — evolution from FSM-controls-conversation to Schema+Policy control obligations, Goal Engine controls agenda, LLM controls conversational realization.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
