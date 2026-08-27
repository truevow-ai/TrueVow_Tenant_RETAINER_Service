---
category: bug
title: "vNext E2E QA - CORE DEFECT: mixed signal ambiguity"
importance: 8
tags: []
file_paths: []
created: 2026-08-12T15:36:38.268041+00:00
updated: 2026-08-12T15:36:38.268041+00:00
memory_id: d3b0ef6c-7936-47ac-8fd1-7a9aaf06cf1e
---

# vNext E2E QA - CORE DEFECT: mixed signal ambiguity

DeterministicFallbackInterpreter mixed-signal check requires 'never' keyword but common ambiguity is 'spoke...but didn't retain'. CandidateValidator has no confidence threshold — 0.5-confidence llm_stub candidates pass validation. Ambiguous input gets authoritative answer.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
