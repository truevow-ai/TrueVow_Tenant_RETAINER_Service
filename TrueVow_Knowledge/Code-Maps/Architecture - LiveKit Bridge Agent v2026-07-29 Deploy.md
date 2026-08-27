---
category: architecture
title: "LiveKit Bridge Agent v2026-07-29 Deploy"
importance: 8
tags: []
file_paths: []
created: 2026-07-30T01:29:17.466037+00:00
updated: 2026-07-30T01:29:17.466037+00:00
memory_id: 5a56b6f7-66d5-47d2-9dfb-03a300983d0d
---

# LiveKit Bridge Agent v2026-07-29 Deploy

6 bridge-level fixes deployed to LiveKit Cloud agent CA_UxWtcHqLEUTp vG934iLXXNzGN: (1) greeting allow_interruptions=False prevents mic-echo cut-off, (2) FAQ bypass injects system message blocking route_workflow when firm policy answers question, (3) _build_collected_data_text filters _seq/_spell/_verify suffix keys and unresolved {template} values, (4) summary node type strips verbose engine data dump from prompt, (5) {placeholder} sanitization removes unresolved templates, (6) ROUTE_HTTP_TIMEOUT_S default raised 8→15s. All tests: 93/93 LiveKit + 40/40 xAI + 14/14 engine passing.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
