---
category: decision
title: "IAM-001: TRACE Clerk-to-Supabase migration complete"
importance: 9
tags: []
file_paths: []
created: 2026-08-03T10:52:02.810418+00:00
updated: 2026-08-03T10:52:02.810418+00:00
memory_id: 6ff5fcbb-18c4-4ad4-a914-44fbfbe66b94
---

# IAM-001: TRACE Clerk-to-Supabase migration complete

Migrated TRACE service from Clerk JWKS to Supabase Auth via truevow_auth (vendored). Replaced AUTH_MODE=clerk with AUTH_MODE=supabase. Removed _JWKSCache class. Renamed clerk_user_id to auth_user_sub in firm_users. Fail-closed — no Clerk fallback. 68/68 tests pass.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
