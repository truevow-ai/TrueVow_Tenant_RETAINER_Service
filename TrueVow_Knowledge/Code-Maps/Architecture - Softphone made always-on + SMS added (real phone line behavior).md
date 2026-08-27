---
category: architecture
title: "Softphone made always-on + SMS added (real phone line behavior)"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T20:28:00.809037+00:00
updated: 2026-07-08T20:28:00.809037+00:00
memory_id: f08426c4-8523-4865-b2bd-af9813fa11dc
---

# Softphone made always-on + SMS added (real phone line behavior)

TrueVow_TWIML_SoftPhone_App upgraded to behave like a always-on phone line for calls AND SMS. (1) ALWAYS-ON: fly.toml auto_stop_machines=off, min_machines_running=1 so inbound call/SMS webhooks always hit a live server; Dockerfile gunicorn pinned to 1 worker + 8 threads (in-memory registry/inbox must be single-process). (2) SMS: new messages.py = Twilio REST send_sms (lazy Client import) + in-memory per-agent inbox (500 cap) + store_inbound routing (assigned agent via registry.resolve_inbound else all online). New routes: POST /sms (Twilio inbound webhook, empty MessagingResponse), POST /sms/send (outbound as logged-in agent), GET /messages?auth=&since= (agent polls, also marks online), POST /messages/read. (3) Frontend: index.html now has Phone/Messages tabs + unread badge; softphone.js keeps Voice device registered ALWAYS with closeProtection + scheduleReconnect on unregistered/error/visibilitychange, polls /messages every 4s, heartbeat /register every 60s, SMS thread UI. (4) Optional webhook security: VALIDATE_TWILIO_SIGNATURE env -> RequestValidator on /voice + /sms (respects X-Forwarded-Proto behind Fly). 26/26 pytest green. Verified live: inbound /sms stored -> agent /messages received it, online_agents=1. Manual: set number's 'A Message Comes In' webhook to /sms, 'A Call Comes In' to /voice; fly secrets need TWILIO_AUTH_TOKEN (for SMS send + sig validation); keep iframe mounted in persistent dashboard layout shell (not a route that unmounts) so registration stays open. Scaling requires moving registry+inbox to Redis.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
