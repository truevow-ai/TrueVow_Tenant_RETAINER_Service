---
category: architecture
title: "Controlled Pilot Architecture Review: Portal scope ownership confirmed"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T04:40:03.682944+00:00
updated: 2026-07-31T04:40:03.682944+00:00
memory_id: 5a9b3475-f633-41c3-9a6c-cac6e24108a3
---

# Controlled Pilot Architecture Review: Portal scope ownership confirmed

RETAINER never grants MATTER_* scopes. SaaS Admin fn_upgrade_portal_access_on_activation correctly adds 5 MATTER_* permissions. Portal upgrade chain intact (previous_grant_id). Contract registry + golden fixtures present and aligned across services. Webhook key isolation intent correct but implementation defect D3 in RETAINER.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
