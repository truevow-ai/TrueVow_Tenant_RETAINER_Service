---
category: architecture
title: "WebhookSignature v1.0 \u2014 INTAKE Fully Compliant"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:41:00.930878+00:00
updated: 2026-07-31T03:41:00.930878+00:00
memory_id: f50f4b9e-542a-49ca-8136-8802079a2819
---

# WebhookSignature v1.0 — INTAKE Fully Compliant

INTAKE now signs all outbound webhooks to RETAINER using HMAC-SHA256 per the frozen WebhookSignature v1.0 contract. Signing string: timestamp:POST:path:body_hash. Headers: X-TrueVow-Key-Id, X-TrueVow-Timestamp, X-TrueVow-Signature. Canonical path: /api/v1/retainer/webhooks/candidate-submitted. Implementation: app/services/voice/bridges/intake_engine/fsm/outbox.py. Golden tests: tests/test_webhook_signature_contract.py — 14/14 pass, covers valid, wrong key, modified body, wrong method/path, trailing slash, expired timestamps, malformed headers, invalid signatures. Legacy bearer auth removed — no migration path needed. Per-service key isolation: key_id=tv-intake-to-retainer-v1 scoped to INTAKE→RETAINER relationship only. Fly secrets: TRUEVOW_WEBHOOK_KEY_ID + TRUEVOW_WEBHOOK_SECRET. Replay protection: event_id UUID per EventEnvelope v1.0.1.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
