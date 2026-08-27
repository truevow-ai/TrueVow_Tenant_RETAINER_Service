---
category: pattern
title: "WorkflowEngine global-intent layer (Phase 1)"
importance: 8
tags: []
file_paths: []
created: 2026-07-14T10:51:05.325989+00:00
updated: 2026-07-14T10:51:05.325989+00:00
memory_id: 9d7c484c-215a-4a36-9cf4-1cfde1e3534b
---

# WorkflowEngine global-intent layer (Phase 1)

process_input now runs a single GLOBAL INTENTS block (turn>0) in locked priority: emergency -> transfer -> identity -> frustration -> ladder. New helpers: _detect_transfer_request (phrase-level w/ lawyer false-positive guard: suppresses 'I already have/hired an attorney','my brother is a lawyer'), _detect_identity_question (are you AI/human/robot, did you hire a human), _detect_frustration (not hearing me/didn't let me finish/keep asking). Identity+frustration re-ask current node via _build_reask_response (no advance). Frustration escape counter: 2 hits at same node -> escalate to callback. Redundant 2nd transfer/emergency block removed. 40/40 test_xai_cloud_bridge.py pass.

---
**Category:** `pattern` | **Importance:** 8/10
**Files:** N/A
