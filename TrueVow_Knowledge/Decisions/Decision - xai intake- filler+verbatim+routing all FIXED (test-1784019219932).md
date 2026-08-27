---
category: decision
title: "xai intake: filler+verbatim+routing all FIXED (test-1784019219932)"
importance: 10
tags: []
file_paths: []
created: 2026-07-14T09:01:34.398207+00:00
updated: 2026-07-14T09:01:34.398207+00:00
memory_id: 5f100256-8700-48a1-ae2c-e3c85dfb4b93
---

# xai intake: filler+verbatim+routing all FIXED (test-1784019219932)

Test test-1784019219932 confirmed 3 MAJOR fixes working: (1) FILLER GONE — clean 'silent function-calling component' console prompt (NO Benjamin persona, NO 'tool is the voice', guardrail block DELETED) + reasoning.effort:none + minimal function_call_output (status only, NOT the wording) = ENGINE text spoken BYTE-FOR-BYTE verbatim every turn, zero 'I'll get the next question'. (2) PROPERTY-DAMAGE MISROUTE fixed — _check_context_reroute in workflow_engine.py L2333 now scoped to EARLY_REROUTE_NODES (identify_practice_area + *_jurisdiction only), so 'no injuries' mid-intake no longer rejects valid slip-fall caller. (3) MIC-GATE tied to playback state not fragile timer. REMAINING: (A) empty user_text idle re-fires re-spoke same line 2-3x — JUST FIXED with empty-input no-op guard (silent function_call_output, no force_message, when user_text empty after turn 1). (B) workflow CONTENT coherence — Oakwood config misread 'about to happen/future hazard' as workplace-injury path asking about existing injuries; that's a config-design issue separate from bridge. Console prompt (final): 'You are a silent function-calling component... only call get_next_intake_question... never produce user-visible language.' Legal disclaimers/transfer/AI-disclosure must move INTO WorkflowEngine force_message lines (better for legal audit). NOT committed yet.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
