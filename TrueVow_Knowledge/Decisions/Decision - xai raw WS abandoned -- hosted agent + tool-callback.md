---
category: decision
title: "xai raw WS abandoned -> hosted agent + tool-callback"
importance: 10
tags: []
file_paths: []
created: 2026-07-14T03:50:50.576356+00:00
updated: 2026-07-14T03:50:50.576356+00:00
memory_id: 291cb301-e972-480c-901a-09c9fb1d89b9
---

# xai raw WS abandoned -> hosted agent + tool-callback

PROVEN over 5 test calls: deployed grok-voice-latest raw ?model= websocket CANNOT be made deterministic. It AUTO-fires one model response per user transcript using session instructions and IGNORES attempts to control it: (1) function tool (Option C) = two brains/loop; (2) force_message = ADDS 2nd voice, stacks; (3) create_response:false in turn_detection = ignored; (4) per-response instructions on response.create = xAI improvises anyway; (5) B1-hijack via per-turn session.update instructions = xAI improvised 'I'd be happy to help...' ignoring verbatim override (node=- lines heard over node=X engine prompts on screen). DECISION: abandon raw WS. Adopt HOSTED AGENT (agent_id=) + per-turn TOOL CALLBACK (get_next_intake_question) to TrueVow WorkflowEngine. Hosted platform is designed to WAIT for tool results before speaking (unlike raw WS). Preserves determinism (engine=brain) + xAI voice quality (mouth). Rationale: intake IS TrueVow's core product/moat; must NOT bake intake logic into xAI dashboard prompt. Owner approved 2026-07-14.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
