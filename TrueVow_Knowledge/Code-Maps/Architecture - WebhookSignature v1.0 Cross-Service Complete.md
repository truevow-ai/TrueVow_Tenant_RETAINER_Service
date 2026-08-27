---
category: architecture
title: "WebhookSignature v1.0 Cross-Service Complete"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:40:57.555656+00:00
updated: 2026-07-31T03:40:57.555656+00:00
memory_id: fd82f1bb-4a43-423c-b332-b01fc9cdabd0
---

# WebhookSignature v1.0 Cross-Service Complete

All 5 backend services now implement WebhookSignature v1.0. INTAKE (14 fixtures), RETAINER (15 fixtures), TRACE (17 fixtures), SETTLE (103 tests), SaaS Admin (16 fixtures, 360-line verifier). Per-service key isolation applied: tv-retainer-to-saas-admin-v1, tv-saas-admin-to-trace-v1 — no global shared secret. Canonical paths frozen. Legacy bearer rejected after 2026-09-01. 3-hop spine: INTAKE→RETAINER→SaaS Admin→TRACE with signed webhooks at each hop.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
