---
category: architecture
title: "SaaS Admin = Platform MDM Control Plane \u2014 INTAKE = Runtime Only"
importance: 10
tags: []
file_paths: []
created: 2026-08-12T13:48:15.117448+00:00
updated: 2026-08-12T13:48:15.117448+00:00
memory_id: eec71c11-43c8-4632-92ec-a60602a8f9e6
---

# SaaS Admin = Platform MDM Control Plane — INTAKE = Runtime Only

SaaS Admin is the platform-wide MDM/control plane (tenant master data, INTAKE Builder, TRACE, SETTLE, Billing, Portal administration, Sales Ops, CRM governance, cross-platform governance). Never part of the real-time voice path. Intake Builder is one SaaS Admin capability among many, not the organizing principle. INTAKE repo houses three planes: Benjamin vNext Core (provider-neutral, Lifecycle FSM/QuestionRunner/Compiler), Bridge Plane (LiveKit/Pipecat adapters), Audio Plane (STT/TTS/VAD/media). Bridge Agent = INTAKE repo workstream, not a separate repo. Runtime path: PSTN/WebRTC → LiveKit → Bridge → Audio → Benjamin Core → Application Plane — all inside INTAKE. SaaS Admin participates out-of-band via MDM/configuration API.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
