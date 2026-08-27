---
category: decision
title: "Client API v1 \u2014 9 Endpoints Frozen"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T02:58:25.839130+00:00
updated: 2026-07-31T02:58:25.839130+00:00
memory_id: 177d0f48-c7a3-4eb2-b20e-c21e23d0dfef
---

# Client API v1 — 9 Endpoints Frozen

RETAINER Client API: 6 GET + 3 POST under /api/v1/retainer/client/v1/. Post-activation: _has_scope maps ENGAGEMENT_HISTORY → ENGAGEMENT_VIEW + COMPLETED_COPY_DOWNLOAD for reads. State-changing endpoints (questions, decline) blocked after activation. DTO allowlists tested via exact-key assertions. Token=v2 (portal access via query param), not lifetime-long bearer.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
