---
category: architecture
title: "First Call Readiness Certificate"
importance: 8
tags: []
file_paths: []
created: 2026-08-12T17:52:00.312668+00:00
updated: 2026-08-12T17:52:00.312668+00:00
memory_id: 36d57256-f5d8-4326-b786-8cd6a39387b6
---

# First Call Readiness Certificate

Tenant publishable only when proven: firm identity valid, tenant active, published intake version valid, practice schema valid, phone/LiveKit routing valid, STT/TTS healthy, answer persistence writable, emergency policy present, conflict-screen strategy present, every policy branch has outcome, effect fallback present. External calendar NOT required — booking unavailable → auto offer callback or internal scheduling. LLM down → deterministic extraction or clarification. CRM down → persist internally + outbox retry. Every dependency has a safe outcome.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
