---
category: architecture
title: "RETAINER: Clerk\u2192Supabase Auth migration complete"
importance: 8
tags: []
file_paths: []
created: 2026-08-03T10:43:39.154044+00:00
updated: 2026-08-03T10:43:39.154044+00:00
memory_id: d6ab6996-a899-451a-abae-656f1144db86
---

# RETAINER: Clerk→Supabase Auth migration complete

Migrated RETAINER Service from Clerk JWKS verification to Supabase Auth via truevow_auth. Replaced app/auth/clerk.py with truevow_auth.verify_supabase_jwt(), updated config.py (clerk_* → supabase_*), updated main.py lifespan with configure() call and AUTH_MODE=supabase enforcement. Fail-closed — no Clerk fallback. Zero Clerk references remain. IAM_MIGRATION_INVENTORY.md and IAM_CLERK_ZERO_REFERENCE_REPORT.md produced in docs/iam/.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
