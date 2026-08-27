---
category: bug
title: "D1: SaaS Admin trailing-slash canonicalization (Severity 2)"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T04:40:15.202178+00:00
updated: 2026-07-31T04:40:15.202178+00:00
memory_id: 2390406b-1852-438a-a27a-fc905be83cd4
---

# D1: SaaS Admin trailing-slash canonicalization (Severity 2)

SaaS Admin webhook-auth.ts:293 strips trailing slashes on verify (path.replace(/\/+$/, '')). Signing for /activate and verifying /activate/ both canonicalize to /activate, defeating wrong-path rejection. Owner: ghous-isb.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
