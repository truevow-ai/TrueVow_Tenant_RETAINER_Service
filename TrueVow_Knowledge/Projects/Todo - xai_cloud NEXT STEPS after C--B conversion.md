---
category: todo
title: "xai_cloud NEXT STEPS after C->B conversion"
importance: 9
tags: []
file_paths: []
created: 2026-07-13T10:16:25.344451+00:00
updated: 2026-07-13T10:16:25.344451+00:00
memory_id: d79d610e-01b9-44cd-8792-7140514061ac
---

# xai_cloud NEXT STEPS after C->B conversion

DONE: C->B force_message conversion, VQM wiring, per-node VAD, missing test helpers (_VOICES/_DEFAULT_VOICE/_build_collected_data_text/_vad_for_node/_VAD_*), frontend rebuild w/ End Call+event log+report download. 40/40 tests pass. NOT YET DONE / NEXT: (1) USER LIVE TEST PENDING on http://127.0.0.1:3023/demo/xai_cloud_test.html — verify no more repetition loop, check transcripts/{sid}-report.json. (2) Add 3-retry-then-escalate guard in WorkflowEngine (industry doc HIGH priority; pushback loops forever currently). (3) 'You mean X?' repair pattern (Dialogflow §2). (4) Preamble/soft-timeout filler on slow LLM-routing nodes (1.5-3.2s classification nodes: conflict_check_prior_rep, opi_jurisdiction). (5) NOT committed yet — commit after successful live test. Ref: docs/VOICE_AI_INDUSTRY_ANALYSIS.md gap table, VOICE_AGENT_CHECKLIST.md §11.

---
**Category:** `todo` | **Importance:** 9/10
**Files:** N/A
