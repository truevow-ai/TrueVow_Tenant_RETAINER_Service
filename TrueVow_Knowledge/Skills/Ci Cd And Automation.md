---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/ci-cd-and-automation/SKILL.md
imported: 2026-08-12T17:53:11.334877+00:00
skill_name: ci-cd-and-automation
---

---
name: ci-cd-and-automation
description: TrueVow Fly.io deployment automation. Use /wizard for interactive deployment scripts. Fly.io-specific deployment patterns.
---

# /ci-cd-and-automation

Fly.io deployment patterns for TrueVow. Use `/wizard` (Pocock) for interactive deployment scripts that walk humans through infrastructure steps.

## Deploy

```bash
fly deploy --ha=false
```

- All services on Fly.io
- Build with Depot (Docker layer caching)
- Rolling strategy with health checks

## Pre-Deploy

Run `/shipping-and-launch` first — it fans out security, review, and tests.

## Per-Service Deploy

```bash
# SaaS Admin
fly deploy --ha=false -a truevow-saas-admin-staging

# Sales Ops
fly deploy --ha=false -a truevow-sales-ops

# INTAKE
fly deploy --ha=false -a truevow-tenant-public

# Billing
fly deploy --ha=false -a truevow-billing-v2
```

## Secrets Management

- **Infisical** (self-hosted) — single source of truth
- Per-trust-domain scoping (App2 never holds App1 secrets)
- Pre-commit hook catches committed secrets
- Set: `fly secrets set KEY=VALUE`
- List: `fly secrets list`
- Never duplicate secrets across services

## Worker Processes

```toml
[processes]
web = "node server.js"
worker = "node scripts/worker.js"
onboarding-worker = "node scripts/plg/onboarding-command-worker.js"
```

Workers must:
- Remove `dotenv` dependency (use Fly secrets)
- Verify DB connectivity at startup
- Fail loudly on missing config (exit 1, not silent start)
- Use pg Pool, not Supabase REST, for Fly→DB access

## Environment Variables

- `TRUEVOW_DEPLOYMENT_ENV` — `staging` | `production` | `development`
- `NODE_ENV` — standard Next.js runtime mode (NOT used for deployment gates)
- Use `TRUEVOW_DEPLOYMENT_ENV` for production-vs-staging authority decisions

## Related
- `/shipping-and-launch` — pre-deploy gate
- `/wizard` — interactive deployment walkthroughs
- `/deprecation-and-migration` — safe data migrations
