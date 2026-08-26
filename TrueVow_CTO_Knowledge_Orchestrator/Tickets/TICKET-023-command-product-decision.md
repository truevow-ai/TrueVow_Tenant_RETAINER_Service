# TICKET-023 — COMMAND product decision (AWAITING FOUNDER)
id: TICKET-023
title: COMMAND service has zero code - decide build vs rename doctrine
repo: COMMAND
status: AWAITING_FOUNDER
depends_on:
goal: GOAL-1
created: 2026-08-26
updated: 2026-08-26
---
Discovered during TICKET-022: TrueVow_Tenant_COMMAND_Service is an empty directory.
No code exists locally or in any sibling repo. Yet the live website doctrine says
"INTAKE captures, TRACE develops, SETTLE resolves, COMMAND measures" and the v4.0
guide lists COMMAND as a service.

Founder must choose ONE:

(a) BUILD NOW - scope what "COMMAND measures" v0 actually does (which metrics,
    from which services), and I will spec + ticket it.
(b) PARK - keep the empty dir, mark it PLANNED everywhere, remove from active registries.
(c) RENAME/RESCOPE - if measurement already happens elsewhere (Platform Analytics?),
    fold the doctrine into that and delete the empty shell.

Reply with a, b, or c.

---

