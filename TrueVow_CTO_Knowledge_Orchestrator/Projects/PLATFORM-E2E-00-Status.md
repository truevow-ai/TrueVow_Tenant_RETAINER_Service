# PLATFORM-E2E-00 — Status Update

> **Date**: 2026-08-04
> **Session**: Active execution

---

## Gates Completed This Session

| Gate | Service | Action | Status |
|------|---------|--------|--------|
| 1 | Billing | Code freeze `6da54b6` | PASS (code) |
| 2 | Sales Ops | Code freeze `7647de2` | PASS (code) |
| 3 | INTAKE | DB migrations + template seed | **PASS** |
| 4 | SaaS Admin | Deploy `1cb75ba` | **PASS** |

## Gate 3 Detail — INTAKE DB

```
4 foundation tables created (intake_templates, intake_template_versions,
  intake_tenant_configurations, intake_provisioning_commands)
2 PLG-INTAKE-01R migrations applied (workflow_path column + template seed)
PI_STANDARD_INTAKE v1.0.0: 1 active row
Checksum: 8fd4c8ab... MATCH
Workflow path: oakwood_law_firm/personal_injury_speech.json
```

## Gate 4 Detail — SaaS Admin

```
Deployed: 1cb75ba → truevow-saas-admin-staging.fly.dev
Migrations 185-187 applied: intake_template_references (3 rows),
  tenant_intake_configuration_projection, intake_customization_requests
```

## Remaining Blockers

| Gate | Service | Blocker | Detail |
|------|---------|---------|--------|
| 3 | INTAKE | No fly.toml | Was removed during Dograh cleanup. `intakely-backend` app exists but is 2 months stale. |
| 5 | FM | No fly.toml or Dockerfile | Code ready at 3f587e5, no deployment config |
| 5 | Billing | No Dockerfile | Has fly.toml, needs Dockerfile for Fly.io build |
| 5 | Sales Ops | npm ci failure | Dockerfile exists but npm ci fails in builder |
| 6 | HMAC | Depends on all deploys | Keys can't be configured until services are running |
| 7 | Preflight | Depends on all deploys | — |
| 8-9 | E2E | Depends on Gates 3-7 | — |

## What Needs Platform Operations

1. Create/recover Fly.toml + Dockerfile for INTAKE (or use existing `intakely-backend` app)
2. Create Fly.toml + Dockerfile for FM
3. Create Dockerfile for Billing (fly.toml exists)
4. Fix Sales Ops npm ci dependency issue
5. Deploy all 5 services to staging
6. Configure HMAC keys
