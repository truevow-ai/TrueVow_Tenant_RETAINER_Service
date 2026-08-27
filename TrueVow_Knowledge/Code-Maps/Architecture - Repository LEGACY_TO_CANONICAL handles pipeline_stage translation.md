---
category: architecture
title: "Repository LEGACY_TO_CANONICAL handles pipeline_stage translation"
importance: 8
tags: []
file_paths: []
created: 2026-08-03T19:36:22.952510+00:00
updated: 2026-08-03T19:36:22.952510+00:00
memory_id: 448a7360-6944-4668-8ea1-d71c0f281443
---

# Repository LEGACY_TO_CANONICAL handles pipeline_stage translation

leads-repository.ts has LEGACY_TO_CANONICAL and LEGACY_TO_TRANSITION maps that auto-translate legacy pipeline_stage writes to canonical states + transitionLead calls. Most write sites go through the repo and are already covered. Direct supabaseAdmin writes still need explicit canonical_pipeline_stage.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
