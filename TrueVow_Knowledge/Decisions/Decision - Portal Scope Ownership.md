---
category: decision
title: "Portal Scope Ownership"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T03:00:36.125566+00:00
updated: 2026-07-31T03:00:36.125566+00:00
memory_id: f4c58cb6-3028-41e3-a319-2ca328806009
---

# Portal Scope Ownership

RETAINER transitions ENGAGEMENT_ONLY to ENGAGEMENT_HISTORY on activation. Shared Platform adds ACTIVE_MATTER after matter.activated. RETAINER never grants MATTER_* scopes. Verified in domain/activation.py:159 and domain/portal.py:27.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
