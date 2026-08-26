# Session Log 2026-08-26 — Uncle Bob Agentic Principles → Gap Analysis → Adoption Tiers

> RESUME POINT: next session starts at **Tier 1 implementation** below.
> Source: Matt Pocock × Uncle Bob Martin video transcript (founder-provided).

## What happened this session (context)

1. CTO Orchestrator v2 shipped & trial-run: `cto_v2.py` (status/next/board/brief/junior/
   canonical/review/integrate/report/shift) + Decision-Map + 10 tickets + regenerated board
   + night-shift.bat launcher. Two bugs found & fixed during trial (brief `_effective`
   KeyError; integrate gate accepted unticked APPROVED — now requires `[x] APPROVED`).
2. TICKET-022 executed manually: RETAINER (125 files, 8259c98) + Platform Analytics
   (83 files, 84fed34) got standalone git + secret guards pre-commit. COMMAND discovered
   EMPTY → TICKET-023 AWAITING_FOUNDER (build / park / rescope — founder hasn't answered).
3. SETTLE JUNIOR-001 loop proven end-to-end with honest REJECT (ruff 2 errors) →
   TICKET-024 filed for the lint fix.

## Extracted implementable principles (summary)

1. Deterministic tools > steering prose ("lost in the middle"; rules = guidelines).
2. The Loop: iterate code until machine verdict says OK.
3. Clean-as-you-go — agents thrash on messy code (threshold differs, wall same).
4. The Gauntlet: Specifier (Gherkin acceptance + QA procedure from human POV) →
   Coder (tests+impl, deliberately messy) → Cleaner (CRAP + cleanup) → Hardener
   (mutation testing, kill all surviving mutants) → QA agent (executable deterministic check).
5. Fresh context per stage (born→task→die); kills trajectory contamination; parallelizable.
6. CRAP score = complexity×coverage; human threshold ~4, agents tolerate 6–8.
7. Human reads scores, never line-by-line code; spot checks only.
8. Dependency-rule file + checker = architecture as law (violations fixed via inversion/
   interface/module split). Architecture viewer for structural inspection.
9. Deep modules: models read interfaces + tests-as-docs, skip implementations.
10. Anti-spec-maxing: big upfront plans fail like waterfall; cost-of-change ≈ $1 →
    thin slices, inspect architecture between slices. END RESULT IS THE SPEC.
11. Persist decisions + acceptance criteria (thin); plans are fuel, decisions are law,
    code+tests are truth. Do not impose human disciplines (TDD ritual) on agents —
    impose values + adjusted thresholds; enforce outcomes.
12. Treat juniors EXACTLY like agents: bounded tasks + same deterministic tools +
    gauntlet residency = how they learn strategy. (= our junior/review/integrate layer.)

## Gap analysis conclusion (vs current stack)

Already aligned: thin-slice doctrine, canonical decisions, juniors-like-agents,
per-service truth commands (defined), personas/skills exist.
Missing: verification EXECUTION in the loop; Gherkin acceptance sections;
stage handoffs; complexity metrics; dependency-rule configs; mutation hardener.

## ADOPTION TIERS (resume here)

### TIER 1 — build next (small, immediate)
- [ ] `verify REPO` command in cto_v2.py: runs config.yaml truth_commands for that
      service (python: pytest/ruff/mypy; ts: lint/typecheck/test/build), captures
      PASS/FAIL + output tail into `.cto-v2-state.json` last-verify per repo.
- [ ] Wire into review gate: `integrate` REFUSES unless last verify for that repo PASS
      (in addition to `[x] APPROVED`).
- [ ] Template tweaks (JUNIOR_TEMPLATE + BRIEF_TEMPLATE):
      (a) Acceptance section in Gherkin form (Given/When/Then);
      (b) outcome-not-ritual wording — "tests exist and pass", drop TDD process mandate;
      (c) one-line constraint: "read tests + interfaces before implementations".
- [ ] Fold last-verify status into `shift` report + Repo Pulse board column.

### TIER 2 — next sprint
- [ ] Dependency-rule configs per repo (import-linter for Python, dependency-cruiser
      for TS) checked as part of verify.
- [ ] radon-based CRAP score surfaced per changed module in reports.

### TIER 3 — later / pilot
- [ ] Mutation-testing hardener stage (mutmut) piloted on small INTAKE validator module only.
- [ ] Full five-role gauntlet automation with fresh-context sub-agent handoffs.

## Open items carried

- TICKET-023 (COMMAND decision: a/b/c) — awaiting founder.
- 9 READY tickets on board incl. hygiene T001–T003, T004/T005 wiring, T010/T011 G13 path,
  T020 auth audit, T021 website QA.
- Commits made this checkpoint: see git log both repos (orchestrator repo + root workspace).
