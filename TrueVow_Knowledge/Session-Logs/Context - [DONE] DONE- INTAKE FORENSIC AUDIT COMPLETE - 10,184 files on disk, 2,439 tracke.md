---
category: context
title: "[DONE] DONE: INTAKE FORENSIC AUDIT COMPLETE | 10,184 files on disk, 2,439 tracked, 16 dirty (7 modified + 9 untra"
importance: 7
tags: ["agent-checkin", "done", "DONE", "TrueVow_Tenant_INTAKE_Service"]
file_paths: []
created: 2026-08-12T04:48:42.994368+00:00
updated: 2026-08-12T04:48:42.994368+00:00
memory_id: b63cea2a-8fcd-4ef4-8621-7b2a705491b3
---

# [DONE] DONE: INTAKE FORENSIC AUDIT COMPLETE | 10,184 files on disk, 2,439 tracked, 16 dirty (7 modified + 9 untra

{"agent_id": "TrueVow_Tenant_INTAKE_Service", "action": "done", "status": "DONE", "message": "INTAKE FORENSIC AUDIT COMPLETE | 10,184 files on disk, 2,439 tracked, 16 dirty (7 modified + 9 untracked). Branch: review/tv-intake-engine-p1-02e-r1. Deployed Fly v157 on truevow-tenant-public. 128 API routes, 5 WS endpoints, 7 workers. 42 ORM models, 36 migrations (0 Alembic, 2 duplicates), 3 portal_* tables missing in staging, 19 tables with ORM/DB skew. 126 state mutations (27 FSM-gated, 1 critical bypass in xai_cloud_voice_bridge). 130+ side effects (6 FSM-gated). 250+ tenant hardcodes (~25 production leaks). 7 FSM implementations (3 active, 4 archived). Workflow: 129 nodes, 116 reachable, 21 orphans (entire OPI sub-workflow unreachable), 22 cycles, 9 broken targets (all sequence-internal). | Learned: Single biggest risks \u2014 Oakwood hardcodes in production prompts, xai_cloud bypass of FSM authority, ORM/DB skew on 19 tables, entire OPI workflow unreachable. | Next: CTO reviews evidence, drives cleanup/certification plan", "timestamp": "2026-08-12T04:48:42.993987+00:00", "working_dir": "C:\\Users\\yasha\\OneDrive\\Documents\\TrueVow\\Cursor\\TrueVow_Tenant_INTAKE_Service"}

---
**Category:** `context` | **Importance:** 7/10
**Files:** N/A
