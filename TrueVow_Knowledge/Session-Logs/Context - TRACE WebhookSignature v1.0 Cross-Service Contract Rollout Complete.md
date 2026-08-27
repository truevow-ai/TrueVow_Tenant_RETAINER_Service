---
category: context
title: "TRACE WebhookSignature v1.0 Cross-Service Contract Rollout Complete"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:42:19.541099+00:00
updated: 2026-07-31T03:42:19.541099+00:00
memory_id: e9d4abaf-5756-475c-823d-a54e6a6b9a7c
---

# TRACE WebhookSignature v1.0 Cross-Service Contract Rollout Complete

All six corrections applied: (1) EventEnvelope v1.0.1 frozen at 18 fields, (2) matter.activated payload normalized to 9 canonical evidence references, (3) webhook auth upgraded from shared-secret to HMAC-SHA256 with X-TrueVow headers, (4) global vs tenant data separation documented, (5) event_id idempotency replay protection added (two-layer: timestamp tolerance + canonical ID), (6) per-link keys replacing global shared secret. 17 golden fixture tests pass. Webhook spine: INTAKE -> signed -> RETAINER -> signed -> SaaS Admin -> signed -> TRACE. Legacy bearer cutoff: 2026-09-01.

---
**Category:** `context` | **Importance:** 10/10
**Files:** N/A
