---
category: decision
title: "xai hosted-agent + force_message = VERBATIM delivery WORKS"
importance: 10
tags: []
file_paths: []
created: 2026-07-14T08:20:51.968182+00:00
updated: 2026-07-14T08:20:51.968182+00:00
memory_id: 23093d54-ca63-4c27-9543-62a033814abb
---

# xai hosted-agent + force_message = VERBATIM delivery WORKS

MILESTONE (test-1784016779016, 19 turns): force_message delivers engine prompts BYTE-FOR-BYTE verbatim. Confirmed AGENT_SPOKE == ENGINE for every node (In what city..., What caused you to slip..., etc). Full coherent intake flow completed greeting->conflict->practice_area->slip_fall->jurisdiction->hazard->witnesses->injuries->contact. Architecture PROVEN: (1) response.function_call_arguments.done -> (2) run WorkflowEngine -> (3) conversation.item.create function_call_output (state) -> (4) conversation.item.create force_message with engine text (verbatim TTS) -> (5) NO response.create. Single-brain achieved: engine decides + force_message speaks. ONLY remaining issue: agent narrates 'I'll get the next question for you' BEFORE calling tool = pre-tool filler, which is a CONSOLE PROMPT problem (not code) per xAI docs — force_message can't stop pre-tool narration. Fix: console agent prompt must say 'You produce ZERO words of your own, never narrate/announce tool calls'. Bridge file complete in xai_cloud_voice_bridge.py open()+_handle_tool_call(). NOT committed yet.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
