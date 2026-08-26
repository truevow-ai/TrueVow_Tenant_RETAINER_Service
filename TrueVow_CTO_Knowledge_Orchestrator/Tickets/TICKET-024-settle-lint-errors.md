# TICKET-024 - SETTLE: resolve 2 ruff unsafe-fix class lint errors
id: TICKET-024
title: SETTLE truth-command red - 2 ruff errors need --unsafe-fixes decision
repo: SETTLE
status: READY
depends_on:
goal: GOAL-1
created: 2026-08-26
updated: 2026-08-26
---
Found by JUNIOR-001 baseline verification: `ruff check .` reports 2 errors that only
auto-resolve with --unsafe-fixes. Inspect both sites manually; apply correct fixes;
re-run full ruff + pytest collect; commit referencing this ticket.

Done means: ruff clean without --unsafe-fixes; evidence in report-back.

---

