---
category: architecture
title: "IAM permission check: requireHITLPermission() uses canonical codes, not hardcoded role lists"
importance: 9
tags: []
file_paths: []
created: 2026-08-03T23:23:12.310981+00:00
updated: 2026-08-03T23:23:12.310981+00:00
memory_id: 874579ff-babc-4669-9577-b6376c10ed61
---

# IAM permission check: requireHITLPermission() uses canonical codes, not hardcoded role lists

requireInternalRole() checks: Supabase session, internal scope, ACTIVE platform_staff_membership, SALES_OPS app grant, assigned role. requireHITLPermission() accepts canonical IAM permission codes (sales_applications.review/approve/reject/request_information). IAM_PERMISSION_ROLE_MAP is a compatibility bridge pending SaaS Admin IAM sync. Commit: c31c233. 677/677 PASS.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
