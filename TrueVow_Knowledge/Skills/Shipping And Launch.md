---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/shipping-and-launch/SKILL.md
imported: 2026-08-12T17:53:12.401361+00:00
skill_name: shipping-and-launch
---

---
name: shipping-and-launch
description: Controlled production deployment with parallel fan-out QA. Codes /code-review, /security-and-hardening, and /tdd into a single gate. Use before any Fly deployment.
disable-model-invocation: true
---

# /shipping-and-launch

Fan-out orchestrator. Runs three reviews in parallel, then gates deployment.

## Flow

```
/shipping-and-launch
  ├── /code-review           (Pocock — Standards + Spec axes)
  ├── /security-and-hardening (TrueVow — platform auth, secrets, injection)
  └── /tdd                   (Pocock — red-green-refactor verification)
       │
       ▼
  All three PASS → approve deployment
  Any FAIL → block, report findings
```

## Pre-Deployment Checklist

1. **Code review clear** — `/code-review` passes on diff since last commit
2. **Security audit clear** — `/security-and-hardening` finds no CRITICAL/HIGH
3. **Tests pass** — `/tdd` confirms green suite for changed modules
4. **Migrations safe** — if migrations exist, `/deprecation-and-migration` validates reversibility
5. **Observability wired** — `/observability-and-instrumentation` confirms key metrics exported

## Deployment

```bash
fly deploy --ha=false
```

- Monitor: `fly logs`
- Health: `fly status`
- Rollback ready: know the previous image tag before deploying

## Platform-Specific Gates

- **Sales Ops:** Cannot deploy if `canonical_pipeline_stage` reset is available in production
- **SaaS Admin:** Cannot deploy if `/tenants/internal` route exists
- **CSM:** Cannot deploy if any tenant creation/activation/billing authority is present
- **INTAKE:** Cannot deploy if PHI appears in logs or URLs

## Output

```
SHIP GATE: PASS / BLOCKED
/code-review:           PASS
/security-and-hardening: PASS (0 critical, 0 high)
/tdd:                   PASS (all suites green)
Deployment:             AUTHORIZED / BLOCKED (<reason>)
```

## Related
- `/ci-cd-and-automation` — deployment mechanics
- `/observability-and-instrumentation` — post-deploy monitoring
