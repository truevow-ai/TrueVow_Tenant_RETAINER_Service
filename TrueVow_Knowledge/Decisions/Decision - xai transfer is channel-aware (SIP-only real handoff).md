---
category: decision
title: "xai transfer is channel-aware (SIP-only real handoff)"
importance: 8
tags: []
file_paths: []
created: 2026-07-14T10:51:01.163161+00:00
updated: 2026-07-14T10:51:01.163161+00:00
memory_id: 98734be1-6c56-4b33-b637-58618a30de69
---

# xai transfer is channel-aware (SIP-only real handoff)

Per xAI SIP docs: a REAL warm transfer requires SIP call_id + POST /v1/realtime/calls/{id}/refer (tel:/sip: target). The cloud demo (WebSocket + agent_id + force_message) has NO call_id and NO refer path, so it CANNOT live-transfer. Compliance: a legal AI implying 'connecting you to an attorney now' when it can't is misrepresentation. Phase 1 _build_transfer_response = honest CALLBACK: acknowledge + route into contact capture (reuses sequence fix) + fire_transfer_notification. Response carries forward-compatible action='callback'/target_uri so a future SIP bridge can refer without engine changes.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
