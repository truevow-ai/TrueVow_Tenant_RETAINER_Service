---
category: convention
title: "Webhook Auth Migration \u2014 HMAC v1.0 + Legacy Bearer"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T02:58:23.129483+00:00
updated: 2026-07-31T02:58:23.129483+00:00
memory_id: 65b1df4d-8209-49d3-8da4-446994a56764
---

# Webhook Auth Migration — HMAC v1.0 + Legacy Bearer

Webhook endpoint accepts both HMAC (X-TrueVow-Key-Id + X-TrueVow-Timestamp + X-TrueVow-Signature) and legacy Bearer. HMAC uses SHA-256 body hash + HMAC-SHA256 signing string (timestamp:method:path:bodyHash), 5-min replay window, constant-time compare. Legacy logs deprecation warning. Key resolution: tv-primary → INTAKE_WEBHOOK_SECRET.

---
**Category:** `convention` | **Importance:** 8/10
**Files:** N/A
