---
category: decision
title: "TRACE Portal Access Ownership Model"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T02:56:04.315281+00:00
updated: 2026-07-31T02:56:04.315281+00:00
memory_id: 09615855-e23c-48ed-8534-7481605aa5d5
---

# TRACE Portal Access Ownership Model

Portal access lifecycle: RETAINER local projection goes ENGAGEMENT_ONLY -> ENGAGEMENT_HISTORY (never MATTER_*). Shared Platform canonical grant adds ACTIVE_MATTER after matter.activated. TRACE stores local ClientAccessProjection as temporary convenience — will switch to Shared Platform API when available. Webhook auth uses X-TrueVow-Key-Id + X-TrueVow-Timestamp + X-TrueVow-Signature HMAC-SHA256 per frozen WebhookSignature v1.0 contract. Env var convention aligned with SaaS Admin: TRUEVOW_WEBHOOK_KEY_ID + TRUEVOW_WEBHOOK_SECRET.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
