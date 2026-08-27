---
category: dependency
title: "WebhookSignature v1.0"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T03:00:39.552064+00:00
updated: 2026-07-31T03:00:39.552064+00:00
memory_id: afedfc55-a7f2-49f9-9de4-6ead84599274
---

# WebhookSignature v1.0

HMAC signing implemented: lib/security/webhook-auth.ts (TS ref), app/auth/deps.py (Python verify). Signing string: timestamp:method:path:bodyHash. Replay protection: 5min window. Key rotation via TRUEVOW_WEBHOOK_SECONDARY_KEYS.

---
**Category:** `dependency` | **Importance:** 9/10
**Files:** N/A
