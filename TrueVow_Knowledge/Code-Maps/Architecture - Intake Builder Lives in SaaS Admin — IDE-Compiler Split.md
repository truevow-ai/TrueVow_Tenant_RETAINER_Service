---
category: architecture
title: "Intake Builder Lives in SaaS Admin \u2014 IDE/Compiler Split"
importance: 10
tags: []
file_paths: []
created: 2026-08-12T13:33:24.585930+00:00
updated: 2026-08-12T13:33:24.585930+00:00
memory_id: a47e1d15-aebb-4180-92d0-5b6b7c57f767
---

# Intake Builder Lives in SaaS Admin — IDE/Compiler Split

SaaS Admin owns the Intake Builder (drag-and-drop canvas, draft editor, SAFE/ADVANCED/SYSTEM lock UX, version history, publish orchestration, CSM approval). INTAKE owns the compiler/runtime (schema validator, template compiler, compiled Benjamin runtime, lifecycle FSM, QuestionRunner). SaaS Admin is the IDE, INTAKE is the compiler. Lock levels (SYSTEM_LOCKED/TEMPLATE_LOCKED/TENANT_CONFIGURABLE) are defined authoritatively by INTAKE's catalogue, rendered by SaaS Admin UI. Publishing crosses the boundary: SaaS Admin edits → requests validation → INTAKE compiles → returns pass/fail + compiled checksum → SaaS Admin approves/publishes → INTAKE creates immutable configuration version. No per-firm containers in INTAKE — shared runtime with tenant_id isolation. Audit existing workflow builder before building new one.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
