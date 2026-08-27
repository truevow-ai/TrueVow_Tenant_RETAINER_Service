---
category: bug
title: "TRACE 9 bugs fixed Jul 24 2026"
importance: 10
tags: []
file_paths: []
created: 2026-07-24T13:48:10.672636+00:00
updated: 2026-07-24T13:48:10.672636+00:00
memory_id: 662a3d1c-eb00-4a76-b31a-9080bc3447b2
---

# TRACE 9 bugs fixed Jul 24 2026

1) extraction_confidence VARCHAR(10->32) overflow on DO_NOT_REQUEST value. 2) audit_log.action VARCHAR(100->255) overflow on long paths. 3) get_case no firm_id filter (SECURITY: firm isolation gap). 4) ChronologyExporter export_json/export_pdf called with wrong params in qa.py. 5) LOCAL_JWT_SECRET not set in .env.local causing auth failure. 6) .env.local @DOCUMENTATION parse error on line 491. 7) Portal proxy returned 401 (no JWT generation). 8) TRACE not visible to non-admin users (no tenantId fallback). 9) Billing proxy fallback missing trace feature. All fixed in code. Schema fixes (#1, #2) still need ALTER TABLE on Supabase production DB.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
