# CONTEXT — TrueVow Platform Glossary

> Canonical terms for the CTO Knowledge Orchestrator and the platform it governs.
> Update in place when a term resolves. No implementation details here.

## The Orchestrator System

- **CTO Orchestrator** — the standing AI replacement for the human CTO seat. Executes
  ready tickets, asks the founder real questions, keeps board/guide/memory truthful.
- **Decision Map** — the current goal tree: goals decomposed into tickets with
  dependency edges. One map at a time.
- **Ticket** — a unit of orchestrator work bound to one repo: status, dependencies,
  brief path, result. States: READY → IN_PROGRESS → DONE (or BLOCKED / AWAITING_FOUNDER /
  SHELVED).
- **Brief** — a work order written into a target repo so that repo's agent can execute
  without knowing the orchestrator exists.
- **Board** — the single kanban view of ticket + service state; refreshed every session.
- **Hygiene Rule** — repos with uncommitted changes are frozen for new assignments
  until changes are COMMIT/PARK/DISCARD-classified; discard needs explicit founder OK.
- **HITL (human-in-the-loop)** — the founder gate: hard-stop operations (production
  deploys, shared-data migrations, secret changes, cross-service contract changes,
  spending) plus platform-clarity questions.
- **Junior Test** — acceptance bar: a fresh agent given only TrueVow_Context answers
  platform-state questions correctly with zero human help.

## Gate Ladders (never conflate)

- **Handoff Commissioning ladder** — Gate 0/0R/1 → Phase 5: Sales Ops → SaaS Admin
  handoff contract commissioning. Gate 0 = blocker audit; Gate 1 = contract freeze;
  Phase 5 = full 62-test commissioning matrix.
- **Tenant G-ladder** — G10 (Sales Ops→SaaS Admin handoff, CLOSED) → G11 (provisioning,
  CONDITIONAL/OPEN) → G11A (billing) → G12 (portal) → G13 (Benjamin INTAKE readiness,
  HOLD pending manual testing as of 2026-08-21) → G14 (controlled tenant activation,
  HARD HOLD) → G15 (revenue assurance).

## The Engine

- **Benjamin** — the voice legal-intake engine (AI receptionist) inside the INTAKE
  service.
- **Schema/Goal core** — canonical Benjamin architecture: facts + goals replace
  questions + states. FactExtractor → CandidateValidator → PolicyEngine → GoalEngine
  → ConversationConductor (LLM conducts within code-determined AllowedAgenda) →
  PlanValidator → typed EffectRequest/EffectResult. Legacy FSM/vNext retired via
  LEGACY-RETIREMENT-05.
- **Hard invariants** — zero question-as-FSM-state; zero LLM direct fact/policy/
  effect/lifecycle authority; LiveKit owns transport only; fail-closed bootstrap;
  provider-neutral core.
- **FirstCallReadiness** — pre-call proof chain: valid tenant, pinned config version +
  checksum, DB reachable; failure means no intake begins.

## Platform

- **Three portals** — Tenant (EXTERNAL), Sales Support/App2 (MEDIUM, LLM zone),
  Platform Operators/App1 (HIGH). SaaS Admin is the MDM control plane; never in the
  real-time voice path.
- **Golden Journey** — prospect → Sales Ops pipeline → T020 human approval → HMAC
  handoff → SaaS Admin commissioning → CSM onboarding → Billing/INTAKE/Portal
  provisioning → controlled activation → product usage (INTAKE captures → RETAINER
  engages → TRACE develops → SETTLE resolves → COMMAND measures) → revenue assurance.
- **WebhookSignature v1.0** — frozen cross-service HMAC contract; per-link key
  isolation (`tv-<caller>-to-<receiver>-v1`); no global shared secret.
- **EventEnvelope v1.1.0** — frozen 18-field event contract; nullable `tenant_id`
  only pre-tenant.
- **RULE 0** — no fabrication. Report only what was directly observed; simulation is
  not commissioning evidence.
- **Living documents (exactly three)** — Developer Guide (TrueVow_Context), CTO
  Orchestrator v2 spec, this glossary. Edited in place; superseded docs get banners.
