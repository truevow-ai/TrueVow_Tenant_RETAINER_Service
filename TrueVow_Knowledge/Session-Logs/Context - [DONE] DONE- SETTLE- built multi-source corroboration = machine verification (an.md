---
category: context
title: "[DONE] DONE: SETTLE: built multi-source corroboration = machine verification (answer to no-human-verifier problem"
importance: 7
tags: ["agent-checkin", "done", "DONE", "TrueVow_Tenant_SETTLE-Service"]
file_paths: []
created: 2026-07-11T07:50:00.457685+00:00
updated: 2026-07-11T07:50:00.457685+00:00
memory_id: bd9d98f3-c291-41bc-a69d-f95c0273c006
---

# [DONE] DONE: SETTLE: built multi-source corroboration = machine verification (answer to no-human-verifier problem

{"agent_id": "TrueVow_Tenant_SETTLE-Service", "action": "done", "status": "DONE", "message": "SETTLE: built multi-source corroboration = machine verification (answer to no-human-verifier problem) | outcome: corroborate_verdicts.py promotes pending->verified ONLY when same case appears in >=2 independent sources (CAP/CourtListener/MoreLaw) agreeing on amount within 1pct, matched by shared reporter citation or name+state+amount; dry-run over 12444 found 1249 corroborated (1248 via citation); spot-check confirmed real matches (Harvey v GEICO 9.2M in CAP+CL, Sanders v ERP 4.5M x3) AND correct rejection of near-miss (RJ Reynolds 20M vs 21M not promoted); 16 CI tests incl corroboration guard | learned: ~10pct of scraped verdicts self-verify via independent-source agreement - no human needed for those; disagreements correctly stay pending | blocker: Supabase pooler (5432) down server-side blocks the DDL migration + live promotion; REST analysis works, will apply on recovery", "timestamp": "2026-07-11T07:50:00.457430+00:00", "working_dir": "C:\\Users\\yasha\\OneDrive\\Documents\\TrueVow\\Cursor\\TrueVow_Tenant_SETTLE-Service"}

---
**Category:** `context` | **Importance:** 7/10
**Files:** N/A
