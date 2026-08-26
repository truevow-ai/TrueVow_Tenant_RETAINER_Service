# Decision Map — current goal tree

> Maintained by CTO Orchestrator v2. Goals decompose into `Tickets/TICKET-*.md`.
> A ticket is READY only when every ticket in its `depends_on` is DONE.
> Regenerate views with: `python TrueVow_Shared_Orchestration/cto_v2.py shift`

## GOAL-1 — Platform Truth Restored

Every repo's state is knowable, saved, and registered; agents inherit truth, not folklore.

```
T001 Hygiene: Sales Ops ─┐
T002 Hygiene: Billing ───┼─ (independent; each unblocks its own repo for assignments)
T003 Hygiene: TRACE ─────┘
T022 Restore standalone .git for RETAINER/COMMAND/Platform Analytics (found via first shift)
T004 Ecosystem config reconciliation (INTAKE rename, RETAINER/COMMAND/Website registration,
     TRACE stale Clerk note fix)
   └─> T005 Wire brief intake into each repo's AGENTS.md (agents discover work orders)
```

## GOAL-2 — G13 Benjamin Qualification Path

```
T010 Complete manual testing of INTAKE engine (founder + INTAKE repo agent)
T011 Staging health re-verification (INTAKE DB connectivity from Fly org)
T010 + T011 ─> T012 Fresh-context G13 qualification (QA mandate bar, P1-P5)
```

G14 stays HARD HOLD regardless of T012 until cross-service governance says otherwise.

## GOAL-3 — Commercial & Web Truth

```
T020 Supabase Auth coverage audit (Billing/FM code reality vs founder decision;
     reconcile TRACE ADR-003 "Clerk platform standard" note)
T021 Website compliance QA (legal/browser review -> lift noindex when green)
```

## GOAL-4 — Junior Developer Management Layer (cto_v2 commands)

```
junior REPO TITLE  -> bounded assignment in <repo>/docs/work-orders/JUNIOR-nnn.md
                      (scope + Definition of Done + constraints; hygiene-frozen repos refused)
review JUNIOR-nnn  -> review artifact in Reviews/ (gates integration)
integrate JUNIOR-nnn -> merge plan; REFUSES until review is APPROVED
canonical KEY "decision" -> Decisions/Canonical-*.md so solved defects cannot be
                      overwritten and reappear (ends the vibecode/Sania loop)
```

## Founder asks currently open

None yet — first shift report will populate this section as AWAITING_FOUNDER tickets appear.
