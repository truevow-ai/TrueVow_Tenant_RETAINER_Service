# SPEC — CTO Orchestrator v2: Master Control Layer for the TrueVow Platform

> Status: AWAITING FOUNDER APPROVAL (approval gate between paper and code)
> Author: CTO Knowledge Orchestrator · 2026-08-24
> Supersedes: the *operational* parts of `.triage.yaml` (its policies carry forward verbatim)
> Related: `TrueVow_Context/2026-08-10-TRUEVOW-DEVELOPER-START-HERE.md` (v4.0 living guide), `CONTEXT.md` (glossary)

---

## Problem Statement

Yasha is a non-technical founder with no technical co-founder. He currently acts as the
human CTO: juggling ~5 active repos at any time, relaying instructions to each repo's
agent, and gluing the platform together by hand. This means:

- He cannot step away to do marketing/founder work without the build stalling.
- When he asks an agent "what is happening in repo X?", he gets weeks-old task lists,
  not current truth — because nothing forces status to be recorded or refreshed.
- Thirteen repos were built as independent services by independent agents; no living
  map ties them into one integrated platform, so integration drifts silently.
- Five orchestration attempts (Obsidian vault → shared memory → shared context →
  Pocock skills → triage YAML) each solved one piece but never operated as a whole,
  because nobody ever wrote down what the orchestrator's job actually is.

## Solution

CTO Orchestrator v2 is the standing replacement for Yasha in the CTO seat. It is a
**ticket-driven, dependency-aware control layer** over all repos:

1. A **Decision Map** decomposes every goal into tickets with explicit dependencies.
2. The orchestrator executes ready tickets by writing a **Brief** into the target
   repo where that repo's agent picks it up, then verifies the return.
3. It works identically whether Yasha is at the keyboard or asleep — schedule or no
   schedule — pausing only to **ask him real questions** (dangerous operations, or
   genuine platform-level ambiguity) via the same ticket mechanism.
4. Every session, it updates the Board, the living Developer Guide, and memory.db so
   the next agent — human or AI, including a brand-new junior agent — inherits
   current truth, not folklore.

## User Stories

1. As the founder, I want to ask "what is happening in repo X?" and get its current
   branch, last commit, dirty-file count, and open tickets — not stale task lists.
2. As the founder, I want to hand the orchestrator a goal and receive a decision map
   of tickets, so I approve direction once instead of supervising every step.
3. As the founder, I want work to continue while I am away, so my absence stops
   blocking engineering.
4. As the founder, I want the orchestrator to ask me questions when *it* hits a
   platform-level ambiguity, so my non-technical judgment is spent only where needed.
5. As the founder, I want dangerous operations (production deploys, DB migrations on
   shared data, secret changes, cross-service contract changes, spending money) to
   always stop and wait for me, so autonomy never becomes exposure.
6. As the founder, I want one screen of "what happened / what's blocked / what needs
   me" after any session, so catching up takes a minute.
7. As the founder, I want unsaved code flagged automatically, so work can't be lost
   or built upon blind.
8. As the founder, I authorized save/park/refactor decisions by agents, but I want
   discard to require my explicit OK, so nothing is destroyed silently.
9. As a repo agent, I want my next assignment delivered as a brief inside my own
   repo, so I never need to know the orchestrator exists.
10. As a repo agent, I want my brief to cite its parent ticket, so my report lands
    back against the right ticket.
11. As a repo agent, I want to refuse new assignments while my repo has unclassified
    dirty files, so I never build on unknown state.
12. As a future junior developer agent, I want one canonical guide that tells me the
    platform, my session protocol, and where current state lives, so I'm useful in
    minutes without asking anyone anything.
13. As a future junior developer agent, I want the guide's "current state" section
    dated and refreshed every session, so I never trust stale facts.
14. As the founder, I want the number of canonical documents fixed and small, updated
    in place forever, so documentation doesn't rot into a pile of contradictory copies.
15. As the orchestrator, I want tickets to declare dependencies, so I execute what's
    unblocked and wait correctly when a dependency isn't done.
16. As the orchestrator, I want every closed ticket to update memory.db, so other
    developers' agents inherit the outcome.
17. As developer sania/ghaus-fsd/ghous-isb, I want the board to reflect reality every
    session regardless of who ran the orchestrator, so coordination doesn't depend on
    Yasha's presence.
18. As the founder, I want the two gate vocabularies (handoff commissioning vs tenant
    G-ladder) kept visibly distinct everywhere, so agents stop conflating them.
19. As the founder, I want the guide to be the single source for binding facts (auth
    provider, service registry, invariants), so contradictions like Clerk-vs-Supabase
    can't recur.
20. As the founder, I want "the junior test" as the definition of done: a fresh agent
    given only TrueVow_Context answers platform-state questions correctly.

## Implementation Decisions

- **Build on existing assets; no parallel systems.** The orchestrator remains
  `TrueVow_Shared_Orchestration/orchestrator.py` plus agent-readable markdown. The
  `.triage.yaml` policies section (git rules, secrets, destructive ops, production
  surface, audit) carries forward verbatim as v2 policy. Obsidian stays as a view;
  memory.db stays as the shared brain; TrueVow_Context stays as the canonical guide
  home. Nothing new competes with these.
- **New artifacts (the v2 seam):**
  - `Decision-Map.md` — current goal tree: goals → tickets → edges (depends_on).
  - `Tickets/TICKET-<n>-<slug>.md` — one file per ticket: id, title, target repo,
    status (`READY / IN_PROGRESS / BLOCKED / AWAITING_FOUNDER / DONE / SHELVED`),
    depends_on list, brief path, result summary, date stamps.
  - Briefs live in the **target repo** (its agent's entrypoint points there);
    a brief cites its ticket id; the closing report must answer: what was proven,
    what ran against real infra, files changed.
- **Highest seam:** the existing session protocol. Start-of-session command sequence
  gains two steps (board refresh + ticket reconciliation); end-of-session gains one
  (state write-back). No daemon, no scheduler required for correctness.
- **Dependency engine:** trivial topological walk. A ticket is READY iff its
  depends_on are all DONE. Blocked/AWAITING tickets are surfaced in the report, never
  silently skipped.
- **HITL contract:** hard-stop list (production deploy, shared-data migration, secret
  change, cross-service contract change, spend) + platform-clarity questions raised as
  AWAITING_FOUNDER tickets phrased in plain language with options and a recommendation.
- **Hygiene rule (founder-approved):** at every session start, repos with uncommitted
  changes are listed and frozen for new assignments until their agent classifies each
  change as COMMIT (with work-order-referencing message), PARK (stash/branch labeled),
  or DISCARD (requires explicit founder verb). Auto-commit is permitted when changes
  cohere with recent commits and verification passes; silent discard is forbidden.
- **Anti-sprawl rule:** exactly three canonical living documents exist — the
  Developer Guide (TrueVow_Context), this spec, CONTEXT.md. They are edited in place,
  versioned by header, and never forked. Any doc older than the guide that overlaps
  it gets a SUPERSEDED banner pointing at the guide.
- **Truth arbitration order when sources conflict:** runtime/git state > memory.db >
  canonical guide > everything else. Conflicts found during scans are filed as tickets.
- **Known corrections baked in:** platform IdP is Supabase Auth (Clerk retired);
  Tenant Application Service repo is now the INTAKE service; RETAINER and COMMAND
  repos exist and join the registry; G13 = HOLD pending manual testing (as of
  2026-08-21); SETTLE idle since Aug 12; Sales Ops/Billing/TRACE carried uncommitted
  work as of 2026-08-23.

## Testing Decisions

Tests verify external behavior of the session protocol, not internals:

- **Junior test (primary acceptance):** fresh-context agent, given only
  TrueVow_Context, correctly reports (a) platform purpose, (b) any named repo's
  current state, (c) which tickets are READY vs blocked, (d) what needs the founder.
  Pass = correct within one session, zero questions to humans.
- **Freshness test:** run scan + board refresh twice, mutate one repo (new commit),
  rerun — board and guide snapshot must reflect the mutation.
- **Freeze test:** dirty a repo, request an assignment targeting it — must be refused
  with classification options.
- **Gate test:** simulate a hard-stop action — must produce an AWAITING_FOUNDER
  ticket and halt, never proceed.
- Prior art: the ecosystem already proves this style via `verify.py` truth-loops and
  check-in protocol; v2 reuses those patterns.

## Out of Scope

- Writing/refactoring service code beyond hygiene handling in the orchestrating repo.
- Autonomous production deploys (forever out — always gated).
- Replacing memory.db, Obsidian, or the per-repo agent harnesses.
- GUI dashboards; markdown board remains the interface.
- Real-time monitoring daemons; the unit of work is the session.
- Completing G13/G14 (those remain owned by the INTAKE qualification track).

## Further Notes

Founder context recorded verbatim for future agents: "I don't have a technical
co-founder who can manage and orchestrate as a whole for me so I can get away-from-
keyboard time to go do marketing activities." That sentence is the spec's reason to
exist. The Pocock "sandcastle" idea (overnight task-runner managing the harness) is
satisfied by the schedule-independent session protocol: any runner — human double-
click, scheduled task, or a person typing one command — triggers the same behavior.
