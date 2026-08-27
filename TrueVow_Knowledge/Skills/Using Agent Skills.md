---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/using-agent-skills/SKILL.md
imported: 2026-08-12T17:53:12.743250+00:00
skill_name: using-agent-skills
---

---
name: using-agent-skills
description: Meta-skill for skill discovery — delegates fundamentals to Pocock, adds TrueVow platform specifics. Use at session start.
disable-model-invocation: true
---

# /using-agent-skills

Two skill families, one workflow. Pocock skills handle engineering fundamentals. TrueVow skills add platform-specific knowledge (SigNoz, Fly, Supabase, Clerk, ontology).

## Session Bootstrap

```
python TrueVow_Shared_Orchestration/orchestrator.py sync-memory
python TrueVow_Shared_Orchestration/orchestrator.py dispatch "<task>"
```

Or ask `/truevow-ask` for a routing recommendation.

## Skill Map — Fundamentals (Pocock) + Platform (TrueVow)

| Phase | Pocock (fundamentals) | TrueVow (platform specifics) |
|-------|----------------------|------------------------------|
| **Align** | `/grill-me` — interview relentlessly | — |
| **Spec** | `/to-spec` — conversation → spec | `/api-and-interface-design` — contract-first + HMAC |
| **Plan** | `/to-tickets` — spec → ticket DAG | — |
| **Build** | `/tdd` — red-green-refactor | `/source-driven-development` — ontology-aware, read-before-write |
| **Verify** | `/code-review` — 2-axis (Standards + Spec) | `/browser-testing-with-devtools` — real browser debugging |
| **Debug** | `/diagnosing-bugs` — disciplined loop | `/observability-and-instrumentation` — SigNoz/Sentry telemetry |
| **Security** | — | `/security-and-hardening` — OWASP, secrets, TrueVow auth |
| **Performance** | — | `/performance-optimization` — Core Web Vitals, Lighthouse |
| **Refactor** | `/improve-codebase-architecture` — deepening survey | `/deprecation-and-migration` — safe data migration |
| **Ship** | — | `/shipping-and-launch` — fans out code-review + security + perf |
| **CI/CD** | — | `/ci-cd-and-automation` — Fly.io + GitHub Actions |
| **Handoff** | `/handoff` — conversation compaction | — |
| **Research** | `/research` — high-trust sources | — |
| **Setup** | `/setup-matt-pocock-skills` — repo config | — |
| **Teach** | `/teach` — multi-session | — |
| **Route** | `/ask-matt` | `/truevow-ask` |

## How They Compose

Always start with the Pocock primitive, then add TrueVow specifics:

```text
/shipping-and-launch      ← calls /code-review + /security-and-hardening + /tdd
/api-and-interface-design ← uses /to-spec, adds contract-first + HMAC
/diagnosing-bugs          ← uses /observability-and-instrumentation for telemetry
/deprecation-and-migration ← uses /to-tickets, adds data safety
```

## Deprecated TrueVow Skills

These TrueVow skills are **replaced by Pocock equivalents**. Keep files for reference, use Pocock versions:

| TrueVow (deprecated) | Use instead |
|----------------------|-------------|
| `test-driven-development` | `/tdd` |
| `code-review-and-quality` | `/code-review` |
| `spec-driven-development` | `/to-spec` |
| `planning-and-task-breakdown` | `/to-tickets` |
| `incremental-implementation` | `/implement` |
| `debugging-and-error-recovery` | `/diagnosing-bugs` |
| `frontend-ui-engineering` | `/prototype` |
| `interview-me` / `idea-refine` | `/grill-me` |
| `context-engineering` | `/domain-modeling` |
| `documentation-and-adrs` | `/grill-with-docs` |
| `code-simplification` | `/improve-codebase-architecture` |
| `git-workflow-and-versioning` | `/resolving-merge-conflicts` |
| `doubt-driven-development` | `/wait-what` |
