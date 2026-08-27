---
category: pattern
title: "xai_cloud VQM + per-node VAD + latency payload"
importance: 8
tags: []
file_paths: []
created: 2026-07-13T10:15:30.314243+00:00
updated: 2026-07-13T10:15:30.314243+00:00
memory_id: 4c388c74-1351-44c4-a194-b2c9009805dd
---

# xai_cloud VQM + per-node VAD + latency payload

xai_cloud bridge now uses shared VoiceQualityMonitor (app/services/voice/quality_monitor.py) like Dograh: start_session on bridge.start_session, WorkflowEvent+LatencyEvent(stage=workflow) per turn, LatencyEvent(stage=total) on first audio (TTFA), end_session builds report. Report saved to transcripts/{sid}-report.json with: metrics(connect_to_xai_ms, greeting_ttfa_ms, turn_ttfas_ms, avg), per-turn breakdown (workflow_ms=our-machine engine compute, ttfa_ms=total, transport_plus_provider_ms=ttfa-workflow=2 network hops+xAI STT/TTS overhead), vqm score, vqm_workflow_report. Per-node VAD: _vad_for_node() -> _VAD_STRUCTURED (2000ms silence) for email/phone/name nodes, _VAD_DEFAULT else; applied dynamically via session.update after each turn. Frontend app/web/xai_cloud_test.html rebuilt: End Call button, realtime event log w/ ms deltas, VQM tile, download report. TROUBLESHOOT FROM: transcripts/{sid}-report.json (authoritative, has node decisions); xAI playground logs only for STT/TTS fidelity cross-check.

---
**Category:** `pattern` | **Importance:** 8/10
**Files:** N/A
