# TICKET-020 — Supabase Auth coverage audit
id: TICKET-020
title: Audit Supabase Auth coverage; reconcile Clerk remnants (incl. TRACE ADR-003)
repo: SaaS Admin
status: READY
depends_on:
goal: GOAL-3
created: 2026-08-24
updated: 2026-08-24
---
Founder ground truth (2026-08-24): Supabase Auth is sole human IdP for every repo.
IAM completion report (2026-08-03) claimed removal across 10 repos, but later docs still
reference Clerk (Billing/FM auth notes; TRACE ADR-003 "Clerk platform standard").

Audit each service repo for live Clerk dependencies (imports, env vars, middleware,
docs claiming authority). Produce a coverage table: service -> IdP reality ->
action needed (none / doc fix / code migration estimate). Code migrations themselves
become separate tickets after founder reviews estimates.

Note: hygiene tickets T001-T003 must land first in frozen repos before deep audits there;
doc-only reconciliation may proceed immediately.

Done means: coverage table committed to memory.db + gaps ticketed.

---

