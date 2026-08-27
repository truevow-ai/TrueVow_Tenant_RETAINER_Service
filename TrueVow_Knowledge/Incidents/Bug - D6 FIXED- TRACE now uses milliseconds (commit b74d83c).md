---
category: bug
title: "D6 FIXED: TRACE now uses milliseconds (commit b74d83c)"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T22:01:58.678653+00:00
updated: 2026-07-31T22:01:58.678653+00:00
memory_id: cab08a62-214d-4ffc-8725-630d5d07dfb5
---

# D6 FIXED: TRACE now uses milliseconds (commit b74d83c)

TRACE timestamp verification updated from seconds to milliseconds, matching frozen WebhookSignature v1.0 contract. SaaS Admin Date.now() (ms) and TRACE time.time() * 1000 (ms) will produce identical canonical signing strings. Owner: yasha.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
