---
category: decision
title: "Per-Service Key Isolation for SETTLE"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:41:08.526267+00:00
updated: 2026-07-31T03:41:08.526267+00:00
memory_id: bd113cd1-ebc7-4f87-a20a-ab09e34adcb4
---

# Per-Service Key Isolation for SETTLE

Implemented per-relationship key registry in WebhookVerifier. Keys now bind to calling_service, receiving_service, allowed_methods, allowed_paths, and enabled flag. A TRACE key must never be accepted on a non-TRACE path even if HMAC is valid. Disabled keys support rotation (old key disabled, new key active). Backward-compatible with global TRUEVOW_WEBHOOK_KEY_ID format. Per spec from SaaS Admin directive.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
