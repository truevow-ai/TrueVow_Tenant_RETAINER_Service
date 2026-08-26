# TICKET-005 — Wire brief intake into per-repo AGENTS.md
id: TICKET-005
title: Point every repo agent at docs/work-orders brief intake
repo: SaaS Admin
status: READY
depends_on: TICKET-004
goal: GOAL-1
created: 2026-08-24
updated: 2026-08-24
---
The orchestrator delivers work via briefs written to <repo>/docs/work-orders/TICKET-*.md.
Agents cannot obey what they never read. Add one stanza to each active repo's AGENTS.md:

"At session start, check docs/work-orders/ for open briefs. If present, execute the
oldest first and end your report with its TICKET id."

Scope: INTAKE, RETAINER, TRACE, SETTLE, Billing, COMMAND, Portal, CSM CORE,
SaaS Admin, Sales Ops, FM, Analytics, Website. Skip archived/dead repos.
Commit each AGENTS.md change with message referencing this ticket.

Done means: all listed repos contain the stanza.

---

