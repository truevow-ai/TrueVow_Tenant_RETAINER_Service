# TICKET-001 — Hygiene classification: Sales Ops (58 uncommitted files)
id: TICKET-001
title: Hygiene classification: Sales Ops 58 uncommitted files
repo: Sales Ops
status: READY
depends_on:
goal: GOAL-1
hygiene: true
created: 2026-08-24
updated: 2026-08-24
---
Sales Ops branch `review/tv-pr-staging-e2e-01r` carries ~58 uncommitted changes with no
record of which work order produced them. Classify every changed file:

1. Inventory the diff; group by apparent intent.
2. For each group decide COMMIT (coherent + verification passes), PARK (branch/stash
   labeled `park/<topic>`), or DISCARD (junk only — requires founder verb, do NOT delete).
3. Commit groups separately with messages referencing this ticket id.
4. Report: per-group decision, evidence, final `git status` clean-or-explained.

Done means: zero unexplained dirty files in the repo.

---

