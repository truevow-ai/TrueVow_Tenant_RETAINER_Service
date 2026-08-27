---
category: decision
title: "BREAKTHROUGH: xai hosted-agent + WS client-function tool WORKS"
importance: 10
tags: []
file_paths: []
created: 2026-07-14T07:52:34.233985+00:00
updated: 2026-07-14T07:52:34.233985+00:00
memory_id: df8b43bc-d5a8-4cae-af5c-b5df0a5af5a8
---

# BREAKTHROUGH: xai hosted-agent + WS client-function tool WORKS

SOLVED after days of raw-WS failure. Working architecture: connect ws ?agent_id=<hosted agent> + send session.update registering a client-side type:function tool 'get_next_intake_question'. Hosted agent (unlike raw ?model=) RELIABLY calls the tool over the SAME websocket via response.function_call_arguments.done (confirmed 8 tool calls in test-1784015193552), waits for function_call_output, then speaks our verbatim next_message. WorkflowEngine stays the brain (local, per _VoiceSession), xAI is mouth+ears. Console GUI only shows server-side 'API request' tools, but WS session.update supports client functions per docs. Key facts: conversation.created->conversation.id is the only stable session key (for resumption); console agent system-prompt must instruct 'call tool with caller EXACT words in user_text every turn, say next_message verbatim, never improvise'. REMAINING: agent sometimes calls tool with empty user_text (fixed: empty input returns CURRENT node prompt, no state change; + stronger prompt). File: xai_cloud_voice_bridge.py open()+_handle_tool_call(). Fallback for Twilio phone path: /api/v1/voice-bridge/hosted-agent/turn HTTP endpoint (needs Fly public deploy).

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
