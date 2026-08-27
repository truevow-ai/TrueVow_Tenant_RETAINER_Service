---
category: bug
title: "NEW: INTAKE timestamp uses seconds instead of milliseconds \u2014 cross-service contract gap"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T05:18:36.003916+00:00
updated: 2026-07-31T05:18:36.003916+00:00
memory_id: fdfcbaa5-6438-4631-8519-1266a4bfbda1
---

# NEW: INTAKE timestamp uses seconds instead of milliseconds — cross-service contract gap

INTAKE outbox.py uses time.time() (seconds) for webhook timestamp. RETAINER and SaaS Admin use time.time() * 1000 (milliseconds). Frozen WebhookSignature v1.0 contract specifies millisecond timestamps. This will cause signature verification failures between INTAKE and RETAINER if not aligned. Owner: ghaus-fsd.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
