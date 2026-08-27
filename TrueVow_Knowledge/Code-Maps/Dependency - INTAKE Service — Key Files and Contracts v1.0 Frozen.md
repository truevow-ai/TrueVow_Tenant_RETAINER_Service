---
category: dependency
title: "INTAKE Service \u2014 Key Files and Contracts v1.0 Frozen"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T03:41:09.173973+00:00
updated: 2026-07-31T03:41:09.173973+00:00
memory_id: 95dcf26b-b39d-4022-8e55-7801534ffeb2
---

# INTAKE Service — Key Files and Contracts v1.0 Frozen

Key files: workflow_engine.py (FSM + confidence gates 0% duplicates), intake_ontology.yaml (17 concepts source of truth), ontology_resolver.py (observation model), outbox.py (HMAC signing), personal_injury_v2.yaml (qualification rules), fsm/ registries (state/transition/event). Contracts: EventEnvelope v1.0.1 (19 fields), WebhookSignature v1.0 (HMAC-SHA256), candidate.submitted_for_representation_review (9-field payload). Tests: 14/14 engine, 14/14 webhook signature, 50 E2E scenarios (0% duplicates, 93% accuracy). Architecture: 5 layers frozen — Benjamin Constitution, FSM Orchestrator, Intake Ontology, Practice Module, Qualification & Scoring. AGENTS.md updated with contract references and critical knowledge.

---
**Category:** `dependency` | **Importance:** 9/10
**Files:** N/A
