# TICKET-025 - Root workspace git remote points at wrong repo (AWAITING FOUNDER)
id: TICKET-025
title: Root workspace origin = RETAINER GitHub repo; CTO folder lacks own .git
repo: SaaS Admin
status: AWAITING_FOUNDER
depends_on:
goal: GOAL-1
created: 2026-08-26
updated: 2026-08-26
---
Discovered during checkpoint (2026-08-26):

1. The ROOT workspace repo (Cursor/, containing ALL tracked service files, memory.db,
   TrueVow_Context) has origin = git@github.com:truevow-ai/TrueVow_Tenant_RETAINER_Service.git.
   Every historical push-memory landed in the RETAINER repo on GitHub. Local history is
   complete - no data lost. But backups are going to a mislabeled destination.
2. TrueVow_CTO_Knowledge_Orchestrator has NO own .git - served by root workspace.
3. Root still tracks deleted old-name paths (TrueVow_Knowledge_Orchestrator/*) from a
   folder rename that never used git mv.

Founder must decide:
(a) Remote strategy: remove origin entirely, or point to a proper private backup repo
    (e.g., truevow-ai/truevow-workspace-backup). Then one governed push re-homes history.
(b) Should CTO_Knowledge_Orchestrator become its own repo like other services?

No pushes performed since discovery. Reply a/b per item.

---

