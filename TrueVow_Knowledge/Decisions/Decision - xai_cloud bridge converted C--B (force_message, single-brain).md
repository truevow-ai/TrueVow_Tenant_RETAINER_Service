---
category: decision
title: "xai_cloud bridge converted C->B (force_message, single-brain)"
importance: 9
tags: []
file_paths: []
created: 2026-07-13T10:15:00.440450+00:00
updated: 2026-07-13T10:15:00.440450+00:00
memory_id: 6c657742-181c-467c-862d-ad3b3b5b3630
---

# xai_cloud bridge converted C->B (force_message, single-brain)

ROOT CAUSE of xai_cloud conversation-quality failures (repetition loop, 'third time you said that'): Option C two-brain architecture. xAI ?model= + process_intake function tool let xAI's LLM compose its OWN reply AND our WorkflowEngine also drove -> they collided. FIX: converted to Option B. xAI = mouth+ears only (STT/VAD/TTS). WorkflowEngine = sole brain. Per turn: xAI input_audio_transcription -> _handle_user_turn -> engine.process_input(text) -> _force_message(prompt) delivered VERBATIM (item.type=force_message, NO response.create per xAI docs). Removed process_intake tool; instructions now minimal identity only + reasoning.effort=none. File: app/services/voice/bridges/xai_cloud_voice_agent/xai_cloud_voice_bridge.py. 40/40 tests pass.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
