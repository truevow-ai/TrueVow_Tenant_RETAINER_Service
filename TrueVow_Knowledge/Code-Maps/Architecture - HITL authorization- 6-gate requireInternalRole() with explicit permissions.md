---
category: architecture
title: "HITL authorization: 6-gate requireInternalRole() with explicit permissions"
importance: 9
tags: []
file_paths: []
created: 2026-08-03T23:12:22.086529+00:00
updated: 2026-08-03T23:12:22.086529+00:00
memory_id: 663dfe71-44af-4bff-9ca4-4ab0baeb3416
---

# HITL authorization: 6-gate requireInternalRole() with explicit permissions

requireInternalRole() now enforces: Supabase identity, email_confirmed_at (rejects service/machine credentials), scope==='internal' (rejects tenant/unknown/service), assigned internal role. requireHITLPermission() adds role-specific gate: sdr/bdr/ae/gtm can review; admin/revops/sales_manager can approve/reject. 8 negative proofs documented. Local dev UUID blocked in prod/staging.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
