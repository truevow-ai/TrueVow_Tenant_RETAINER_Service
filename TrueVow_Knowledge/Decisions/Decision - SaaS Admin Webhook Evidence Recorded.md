---
category: decision
title: "SaaS Admin Webhook Evidence Recorded"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T03:41:50.144264+00:00
updated: 2026-07-31T03:41:50.144264+00:00
memory_id: 1bfe4b38-2d9a-4b9e-b872-9b59123446f8
---

# SaaS Admin Webhook Evidence Recorded

SaaS Admin verifier: lib/security/webhook-auth.ts (360 lines), 16 golden fixtures at tests/security/webhook-signature.test.ts. Idempotency via command_id replay protection. Raw-body hashing (no JSON re-serialize). timingSafeEqual guard against length mismatch. Canonical paths: POST /api/v1/matters/activate (verify), POST /api/v1/matters/activated (sign). Per-relationship keys. Legacy auth rejected after 2026-09-01.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
