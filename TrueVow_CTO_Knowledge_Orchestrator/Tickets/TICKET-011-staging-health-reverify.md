# TICKET-011 — Staging health re-verification (INTAKE DB connectivity)
id: TICKET-011
title: Re-verify staging health incl. INTAKE DB from Fly org network path
repo: INTAKE
status: READY
depends_on:
goal: GOAL-2
created: 2026-08-24
updated: 2026-08-24
---
Last recorded state (TV-PR-PHASE-01E, Aug 5): 4/5 healthy; INTAKE DEGRADED with DB
unreachable from the "personal" Fly org network path; asyncpg pool singleton does not
retry after secret changes. Since then much changed (Retirement-05, booking deploy).
Re-run preflight now: process healthy, database connected, repository query works,
FirstCallReadiness works (QA mandate §44 bar).

If the org/network root cause persists, propose fix options as AWAITING_FOUNDER ticket
(moving app between Fly orgs affects billing/deployment ownership = founder decision).

Done means: fresh health evidence table for all five staging apps, dated today.

---

