---
category: decision
title: "WebhookSignature v1.0 Hardening + Canonical Paths"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:21:02.458266+00:00
updated: 2026-07-31T03:21:02.458266+00:00
memory_id: b29dd154-082a-478c-aee5-741289994431
---

# WebhookSignature v1.0 Hardening + Canonical Paths

Applied SaaS Admin authoritative corrections to SETTLE: (1) Legacy cutoff corrected to 2026-09-01 per admin directive. (2) Added CANONICAL_PATHS, SERVICE_WEBHOOK_RESPONSIBILITIES, and WEBHOOK_SIGNATURE_CANONICAL_RULES to contracts.py. (3) Added 2 legacy migration tests (cutoff date verification). (4) WebhookVerifier hardened with signature hex format validation, buffer-length guard before compare_digest, idempotency via event_id, auth_source tracking. (5) 17+ golden fixture tests covering all 16 SaaS Admin categories.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
