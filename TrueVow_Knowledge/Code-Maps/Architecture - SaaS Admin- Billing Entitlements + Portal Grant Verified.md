---
category: architecture
title: "SaaS Admin: Billing Entitlements + Portal Grant Verified"
importance: 9
tags: []
file_paths: []
created: 2026-08-01T03:52:01.626425+00:00
updated: 2026-08-01T03:52:01.626425+00:00
memory_id: 3cfb016f-8528-4363-ac80-90f351fba99f
---

# SaaS Admin: Billing Entitlements + Portal Grant Verified

Migration 175: 1727 product entitlements across 578 tenants. Portal grant transition: 9/9 assertions PASS with relational fixture. PROSPECTIVE_ENGAGEMENT → READ_ONLY_HISTORY → ACTIVE_MATTER with all 5 MATTER permissions. Trigger copies portal_identity_id. Activation routes switched from Clerk to HMAC. /ready endpoint verifies 37 tables + 7 functions. RC v3: Engineering APPROVED.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
