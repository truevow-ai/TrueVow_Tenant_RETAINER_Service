---
category: decision
title: "Portal Scope Ownership \u2014 Shared Platform vs RETAINER"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T02:58:19.471136+00:00
updated: 2026-07-31T02:58:19.471136+00:00
memory_id: c6f2497c-06f6-416a-bc96-66c0391803e2
---

# Portal Scope Ownership — Shared Platform vs RETAINER

RETAINER stores local projection (ClientPortalAccess) with canonical_access_grant_id for reconciliation. RETAINER grants ENGAGEMENT_HISTORY on activation, never MATTER_*. Shared Platform owns canonical grants, identities, invitations, and adds ACTIVE_MATTER after matter.activated. ClientPortalAccess.state separated from .scopes (PENDING_INVITATION/ACTIVE/REVOKED vs ENGAGEMENT_VIEW/ENGAGEMENT_HISTORY).

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
