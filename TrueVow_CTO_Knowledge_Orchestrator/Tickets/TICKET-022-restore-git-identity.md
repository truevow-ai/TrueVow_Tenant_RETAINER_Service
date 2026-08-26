# TICKET-022 — Restore standalone git identity for absorbed repos
id: TICKET-022
title: Restore standalone .git for RETAINER, COMMAND, Platform Analytics
repo: RETAINER
status: READY
depends_on:
goal: GOAL-1
created: 2026-08-24
updated: 2026-08-24
---
Discovered by first cto_v2 shift (2026-08-24): TrueVow_Tenant_RETAINER_Service,
TrueVow_Tenant_COMMAND_Service, and TrueVow_Platform_Analytics_Service have NO own
.git directory — their file changes land inside the root Cursor workspace repo, so they
have no independent history, branches, or remote. This repeats the June 2026 "4 services
have NO git repo" defect class.

Protocol (per repo):
1. Check root .gitmodules + remote config to learn the intended upstream (submodule?
   independent repo?). Check GitHub/org for an existing remote with history.
2. If a remote exists: re-attach/clone WITHOUT overwriting local files; reconcile.
3. If no remote exists: secrets-scan the tree FIRST, then `git init` + initial commit
   capturing current state, create private remote on the org, push, then add to
   .gitmodules or ecosystem registry per TICKET-004 conventions.
4. Never delete any source file during recovery.

Done means: all three repos have own .git with clean initial history and a remote,
and cto_v2 status shows them as normal repos.

---


## Result (2026-08-26)

- RETAINER: git restored, 125 files, root commit 8259c98, secret guard added to .gitignore. NOTE: prior history lives inside the root workspace repo (RETAINER was root-tracked); standalone history starts today.
- Platform Analytics: git restored, 83 files, root commit 84fed34; was already root-ignored so no duplication.
- COMMAND: directory is EMPTY - no code exists locally or in any sibling repo. Website doctrine references it. Escalated as TICKET-023 (founder decision).
- Remotes NOT created (needs founder GitHub org choice). Follow-up noted.

