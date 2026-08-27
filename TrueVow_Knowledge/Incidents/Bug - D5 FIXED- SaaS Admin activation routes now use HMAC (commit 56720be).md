---
category: bug
title: "D5 FIXED: SaaS Admin activation routes now use HMAC (commit 56720be)"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T22:01:57.592508+00:00
updated: 2026-07-31T22:01:57.592508+00:00
memory_id: 6852eba9-7a97-4dd8-a4d2-0d292d7e7f8e
---

# D5 FIXED: SaaS Admin activation routes now use HMAC (commit 56720be)

Both POST /api/v1/matters/activate and GET /api/v1/matters/resolve-config now use HMAC WebhookSignature v1.0, not Clerk withAuth. Allowed keys: tv-retainer-to-saas-admin-*. Idempotency: command_id replay returns prior result. Raw body verified before JSON.parse. 68/68 tests pass, 17/17 golden fixtures pass. Owner: ghous-isb.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
