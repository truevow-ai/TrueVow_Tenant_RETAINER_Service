---
category: architecture
title: "PLG-SO-02C: IAM authorization \u2014 5-gate requireInternalRole() + canonical permission codes"
importance: 9
tags: []
file_paths: []
created: 2026-08-05T07:37:41.280879+00:00
updated: 2026-08-05T07:37:41.280879+00:00
memory_id: cf3141f0-b1ff-4232-ad9d-6a9659417603
---

# PLG-SO-02C: IAM authorization — 5-gate requireInternalRole() + canonical permission codes

requireInternalRole(): Supabase session → internal scope → active platform_staff_membership → SALES_OPS app grant → assigned role. requireHITLPermission() uses canonical codes (sales_applications.review/approve/reject/request_information). IAM_PERMISSION_ROLE_MAP is compatibility bridge pending SaaS Admin IAM. Frozen baseline: commit c31c233, migrations 181/182 checksum-frozen. Staging handoff: docs/plg/PLG-SO-02C-STAGING-HANDOFF.md.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
