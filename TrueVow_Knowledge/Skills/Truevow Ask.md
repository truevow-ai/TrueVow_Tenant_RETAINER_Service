---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/truevow-ask/SKILL.md
imported: 2026-08-12T17:53:12.683038+00:00
skill_name: truevow-ask
---

---
name: truevow-ask
description: Route any task to the right TrueVow + Pocock skill. Use when unsure which skill fits.
disable-model-invocation: true
---

# /truevow-ask

Route your request to the right skill. Maps TrueVow platform-specific concerns and delegates fundamentals to Pocock skills.

## Quick Dispatch

| You say | Load |
|---------|------|
| "review this code" | `/code-review` → then `/security-and-hardening` for auth/secrets |
| "write tests" | `/tdd` |
| "security audit / vulnerability" | `/security-and-hardening` → compose with `/code-review` |
| "performance / slow / optimize" | `/performance-optimization` |
| "ship / launch / deploy" | `/shipping-and-launch` → fans out `/code-review` + `/security-and-hardening` + `/tdd` |
| "new feature / spec / define" | `/to-spec` |
| "plan / breakdown / tasks" | `/to-tickets` |
| "implement / build / develop" | `/implement` → uses `/tdd` internally |
| "bug / broken / debug / fix" | `/diagnosing-bugs` |
| "simplify / refactor / messy" | `/improve-codebase-architecture` |
| "api / endpoint / contract" | `/api-and-interface-design` |
| "ui / frontend / component" | `/prototype` |
| "research / search / investigate" | `/research` |
| "setup / configure repo" | `/setup-matt-pocock-skills` |
| "handoff to another agent" | `/handoff` |
| "observability / monitoring" | `/observability-and-instrumentation` |
| "ci/cd / deployment / Fly" | `/ci-cd-and-automation` |
| "deprecate / migrate / remove" | `/deprecation-and-migration` |
| "browser test / devtools" | `/browser-testing-with-devtools` |
| "read source / understand codebase" | `/source-driven-development` |
| "teach me / learn" | `/teach` |
| "align on idea / grill me" | `/grill-me` |

## How Skills Compose

Platform skills compose with Pocock primitives, not replace them:

```text
/shipping-and-launch
  → /code-review (Pocock)
  → /security-and-hardening (TrueVow — adds platform-specific checks)
  → /tdd (Pocock)
  → /ci-cd-and-automation (TrueVow — Fly deployment specifics)

/api-and-interface-design
  → /to-spec (Pocock)
  → TrueVow contract-first + HMAC patterns

/diagnosing-bugs
  → /observability-and-instrumentation (TrueVow — SigNoz/Sentry telemetry)
  → /browser-testing-with-devtools (TrueVow — real browser)
```

## Reference

- TrueVow platform skills: `/security-and-hardening` `/performance-optimization` `/observability-and-instrumentation` `/shipping-and-launch` `/ci-cd-and-automation` `/api-and-interface-design` `/source-driven-development` `/deprecation-and-migration` `/browser-testing-with-devtools`
- Pocock fundamentals: skills in `pocock/` directory
- Orchestrator: `python TrueVow_Shared_Orchestration/orchestrator.py dispatch "<task>"`
