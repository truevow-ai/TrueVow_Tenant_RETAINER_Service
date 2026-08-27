# Gate 1 Platform Operations Environment Audit

> **Date:** 2026-08-02
> **Role:** Platform Operations (read-only audit)
> **Scope:** SaaS Admin + Sales Ops repos — staging environment readiness
> **Mutation:** NONE (read-only)

---

## 1. Supabase Projects

### SaaS Administration Service

| Item | Status | Detail |
|------|--------|--------|
| Config file | **MISSING** | No `supabase/config.toml` exists |
| Project reference | **EXISTS** | `.env.local` line 31: `SAAS_ADMIN_PROJECT_ID=jahhqcypxjkxwrfzpyxd` |
| Project URL | **EXISTS** | `.env.local` line 32: `https://jahhqcypxjkxwrfzpyxd.supabase.co` |
| Staging vs Production | **EXISTS BUT MISCONFIGURED** | Same project (`jahhqcypxjkxwrfzpyxd`) used for both dev and staging. `.env.staging` line 7 uses the same project via pooler. No separate staging Supabase project exists. |

### Sales Ops Service

| Item | Status | Detail |
|------|--------|--------|
| Config file | **EXISTS** | `supabase/config.toml` (project_id = `"TrueVow_Sales_Ops_Service"` — local dev only) |
| Project reference | **EXISTS** | `.env.local` line 34: `SUPABASE_URL=https://bpzegquhxnygyxdzluyw.supabase.co` |
| Project URL | **EXISTS** | `.env.local` line 34 |
| Staging vs Production | **PRODUCTION ONLY** | Same project (`bpzegquhxnygyxdzluyw`) for dev, staging, and production. `fly.toml` line 11 sets the same Supabase URL for production build. No separate staging project. |

### Project-Environment Mapping (Summary)

| Service | Dev | Staging | Production | Supabase Project ID |
|---------|-----|---------|------------|---------------------|
| SaaS Admin | `jahhqcypxjkxwrfzpyxd` | `jahhqcypxjkxwrfzpyxd` (same) | `jahhqcypxjkxwrfzpyxd` (same) | `jahhqcypxjkxwrfzpyxd` |
| Sales Ops | `bpzegquhxnygyxdzluyw` | `bpzegquhxnygyxdzluyw` (same) | `bpzegquhxnygyxdzluyw` (same) | `bpzegquhxnygyxdzluyw` |

**Risk:** Both services use a single Supabase project for all environments. Staging tests run against the same database as development/production.

---

## 2. Migration History

### SaaS Admin — `supabase/migrations/`

| Migration | File | Status | Lines |
|-----------|------|--------|-------|
| 176a | `176_onboarding_milestones_seed.sql` | **EXISTS** | N/A (checked by name) |
| 176b | `176_salesops_golden_fixtures_and_handoff_contract.sql` | **EXISTS** | N/A (checked by name) |
| 177 | `177_transactional_handoff_rpc.sql` | **EXISTS** | 204 lines |

**Note:** Two files prefixed `176_` exist (milestones seed + golden fixtures). Both are migration 176.

### Sales Ops — `supabase/migrations/`

| Migration | File | Status | Lines |
|-----------|------|--------|-------|
| 177 | `20260801000002_migration_177_canonical_states.sql` | **EXISTS** | 198 lines |
| 178 | `20260801000003_migration_178_approval_authority_backfill.sql` | **EXISTS** | 87 lines |

**Note:** Migration 178 includes a production guard (`app.environment = 'production'` check at line 20-22) that prevents execution in production without explicit CTO authorization.

---

## 3. Existing Environment Variables

### `SAAS_ADMIN_STAGING_DATABASE_URL`

| Location | Status | Value / Line |
|----------|--------|--------------|
| `.env.staging` (SaaS Admin) | **SET** | Line 7: `postgresql://postgres.jahhqcypxjkxwrfzpyxd:Intakely%40786@aws-0-us-east-1.pooler.supabase.com:6543/postgres` |
| `.env.local` (SaaS Admin) | **NOT SET** | Variable not present |
| Shell environment | **REQUIRED** | Scripts read from `process.env`, not from `.env.staging` file |

### `SALES_OPS_STAGING_DATABASE_URL`

| Location | Status | Value / Line |
|----------|--------|--------------|
| `.env.staging` (SaaS Admin) | **SET** | Line 10: `postgresql://postgres.bpzegquhxnygyxdzluyw:Intakely%40786@aws-1-us-east-1.pooler.supabase.com:5432/postgres` |
| `.env.local` (SaaS Admin) | **NOT SET** | Variable not present |
| Sales Ops `.env.local` | **NOT SET** | Variable not present |
| Sales Ops `.env.staging` | **MISSING** | No `.env.staging` file exists in Sales Ops repo |
| Shell environment | **REQUIRED** | Scripts read from `process.env`, not from `.env.staging` file |

### `TRUEVOW_WEBHOOK_SECRET_SALES_OPS`

| Location | Status | Value / Line |
|----------|--------|--------------|
| `.env.staging` (SaaS Admin) | **SET** | Line 13: `9b0d41394d929f6f8168f1b4a24c2c30280d9303eaf5d9fb86a984e1189ae398` |
| `.env.local` (SaaS Admin) | **NOT SET** | Variable not present |
| Sales Ops `lib/env.ts` | **NOT DEFINED** | Not in the Zod schema — Sales Ops doesn't yet know about this secret |
| Sales Ops `.env.local` | **NOT SET** | Variable not referenced |

### `SAAS_ADMIN_BASE_URL`

| Location | Status | Value / Line |
|----------|--------|--------------|
| `.env.staging` (SaaS Admin) | **SET** | Line 16: `http://localhost:3001` |
| `.env.local` (SaaS Admin) | **NOT SET** | Variable not present |
| Scripts (default) | **DEFAULTABLE** | Preflight defaults to `http://localhost:3000`; cross-repo integration test defaults to `http://localhost:3000` |

**Critical gap:** `.env.staging` exists with correct values but the Phase 4 scripts (`preflight-check.js`, `staging-failure-injection.js`, `cross-repo-integration-test.js`, `run-gate1-staging.sh`) do NOT auto-load `.env.staging`. All four read directly from `process.env`. The user must manually source/export these variables before running any script.

### Other Staging-Related Variables Found

| Variable | Location | Value |
|----------|----------|-------|
| `SAAS_ADMINISTRATION_SERVICE_ENVIRONMENT` | SaaS Admin `.env.local` line 11 | `development` |
| `SALES_OPS_SERVICE_ENVIRONMENT` | Sales Ops `.env.local` line 11 | `development` |
| `SENTRY_ENVIRONMENT` | Both repos | `development` |
| `WORKFLOW_GIT_BRANCH` | SaaS Admin `.env.local` line 534 | `staging` |
| `NODE_ENV` | Sales Ops `fly.toml` line 21 | `production` |
| `DEMO_COMPLETED_WEBHOOK_SECRET` | Sales Ops `.env.local` line 381 | `truevow-demo-webhook-hmac-secret-2026` |
| `APPLICATION_DECISION_WEBHOOK_SECRET` | Sales Ops `.env.local` line 385 | `truevow-app-decision-webhook-hmac-2026` |

---

## 4. Staging Scripts

All four scripts exist in `TrueVow_SaaS_Administration_Service\scripts\phase-4\`:

| Script | Status | Lines | Notes |
|--------|--------|-------|-------|
| `preflight-check.js` | **EXISTS** | 138 lines | 13 checks; reads env vars from `process.env` |
| `run-gate1-staging.sh` | **EXISTS** | 118 lines | Bash orchestrator; requires manual env export |
| `staging-failure-injection.js` | **EXISTS** | (verified by glob) | Database failure injection at 8 points |
| `cross-repo-integration-test.js` | **EXISTS** | (verified by glob) | 10 integration scenarios |

All scripts are in the SaaS Admin repo. No equivalent scripts exist in the Sales Ops repo. Scripts use `#!/usr/bin/env node` or `#!/usr/bin/env bash` — executable on Unix. On Windows (current environment), `.sh` scripts require WSL or Git Bash.

---

## 5. `fn_process_handoff()` — SQL Function

| Status | **EXISTS** |
|--------|-----------|
| File | `TrueVow_SaaS_Administration_Service\supabase\migrations\177_transactional_handoff_rpc.sql` |
| Definition | Line 28: `CREATE OR REPLACE FUNCTION fn_process_handoff(...)` |
| Parameters | 18 parameters (handoff_id, checksum, firm info, contact info, entitlements, etc.) |
| Return type | `JSONB` |
| Comment | Line 188-189 (verified via grep) |
| Companion table | `handoff_acknowledgments` — created in same migration (line 14) |

The function is defined in the migration file. Whether it has been applied to the staging database depends on whether migration 177 was run against `jahhqcypxjkxwrfzpyxd`.

---

## 6. Existing Staging HMAC Key

| Status | **EXISTS** |
|--------|-----------|
| Location | SaaS Admin `.env.staging` line 13 |
| Value | `9b0d41394d929f6f8168f1b4a24c2c30280d9303eaf5d9fb86a984e1189ae398` (64 hex chars) |
| Consumed by | `lib/security/webhook-auth.ts` line 57: `process.env.TRUEVOW_WEBHOOK_SECRET_SALES_OPS` |

Other webhook secrets found in Sales Ops `.env.local`:
- `DEMO_COMPLETED_WEBHOOK_SECRET=truevow-demo-webhook-hmac-secret-2026` (line 381)
- `APPLICATION_DECISION_WEBHOOK_SECRET=truevow-app-decision-webhook-hmac-2026` (line 385)

Neither of these is the Gate 1 handoff HMAC secret. The handoff secret (`TRUEVOW_WEBHOOK_SECRET_SALES_OPS`) exists only in `.env.staging`, not in any `.env.local`.

---

## 7. Deployment Configuration

### SaaS Admin

| Config | Status | Detail |
|--------|--------|--------|
| `fly.toml` | **MISSING** | SaaS Admin is NOT deployed on Fly.io |
| `vercel.json` | **EXISTS** | Contains only cron config: credential vault key rotation (`0 2 * * *`) |
| `Dockerfile` | **MISSING** | No Dockerfile found |
| `docker-compose` | **MISSING** | No docker-compose files |
| Staging URL | **NOT DEFINED** | Only `http://localhost:3001` in `.env.staging` |

### Sales Ops

| Config | Status | Detail |
|--------|--------|--------|
| `fly.toml` (main) | **EXISTS** | App: `truevow-sales-ops`, Region: `iad`, Port: 3056, URL: `https://truevow-sales-ops.fly.dev` |
| `fly.toml` (email-verifier) | **EXISTS** | App: `reacher-truevow`, Port: 8080, Region: `iad` |
| `vercel.json` | **EXISTS** | Cron: demo-watchdog every 2 min (`*/2 * * * *`) |
| `Dockerfile` | **EXISTS** | Dockerfile found in root |
| `docker-compose` | **EXISTS** | 3 files: `docker-compose.law-firm-pipeline.yml`, `docker-compose.email-verifier.yml`, `docker-compose.email-services.yml` |
| Production URL | **DEFINED** | `fly.toml` line 17: `NEXT_PUBLIC_APP_URL = "https://truevow-sales-ops.fly.dev"` |
| Staging URL | **NOT DEFINED** | No staging-specific deployment configuration |

---

## 8. Secret Management

### Infisical

| Repo | Status | Detail |
|------|--------|--------|
| SaaS Admin | **MISSING** | No Infisical references found in any config files |
| Sales Ops | **MISSING** | No Infisical references found in any config files |

### `.gitignore` — Secret Protection

| Pattern | SaaS Admin | Sales Ops |
|---------|------------|-----------|
| `.env*.local` | Line 40: `# Environment Variables or Secrets or local env files` | Line 30: `# local env files` |
| `.env.local` | Line 41: explicit entry | Line 30: covered by `.env*.local` |
| `.env` | Line 42: explicit entry | Line 31: explicit entry |
| `.env.staging` | **NOT IGNORED** — only `.env*.local` is covered | No `.env.staging` exists |
| Credential files | Lines 131-137: `credentials.json`, `token.json`, `*.pem`, `*.key`, `api_keys_generated.json` | Lines 22, 94: `*.pem`, `data/scraped-leads/twilio_lookup_cache.json` |

**Critical finding:** `.env.staging` is **NOT** covered by either `.gitignore`:
- SaaS Admin `.gitignore`: `.env*.local` pattern matches `.env.local`, `.env.development.local`, etc. but does NOT match `.env.staging`.
- `.env.staging` currently contains a live HMAC secret (`TRUEVOW_WEBHOOK_SECRET_SALES_OPS`) and database connection strings with embedded passwords.
- The file header says "DO NOT COMMIT" but nothing prevents it from being committed.

---

## Summary of Findings

| # | Check | Classification | Key Detail |
|---|-------|---------------|------------|
| 1 | Supabase projects | **EXISTS BUT MISCONFIGURED** | Single project per service across all environments. No separate staging projects. |
| 2 | Migration 176/177 (SaaS Admin) | **READY** | All three migration files exist |
| 3 | Migration 177/178 (Sales Ops) | **READY** | Both migration files exist; 178 has production guard |
| 4 | `SAAS_ADMIN_STAGING_DATABASE_URL` | **EXISTS IN FILE ONLY** | In `.env.staging`; not loaded by scripts automatically |
| 5 | `SALES_OPS_STAGING_DATABASE_URL` | **EXISTS IN FILE ONLY** | In `.env.staging`; Sales Ops repo has no `.env.staging` |
| 6 | `TRUEVOW_WEBHOOK_SECRET_SALES_OPS` | **EXISTS IN FILE ONLY** | 64-char hex key in `.env.staging`; Sales Ops `env.ts` schema doesn't define it |
| 7 | `SAAS_ADMIN_BASE_URL` | **EXISTS IN FILE ONLY** | `http://localhost:3001` in `.env.staging`; scripts default to `:3000` |
| 8 | Staging scripts (preflight) | **READY** | All 4 scripts present with content |
| 9 | `fn_process_handoff()` | **READY** | Defined in migration 177 at line 28; 18 params, JSONB return, transactional |
| 10 | Staging HMAC key | **EXISTS** | Generated and stored, but not synced to Sales Ops env schema |
| 11 | Deployment config | **PRODUCTION ONLY** | SaaS Admin has no Fly/Docker config. Sales Ops has Fly production config only. |
| 12 | Secret management | **NEEDS ATTENTION** | No Infisical. `.env.staging` contains live secrets and is NOT in `.gitignore`. |

---

## Action Items (NON-MUTATION — for CTO review)

1. **CRITICAL:** Add `.env.staging` to `.gitignore` in both repos (currently contains live HMAC key + DB passwords)
2. **HIGH:** Scripts (`preflight-check.js`, `run-gate1-staging.sh`, etc.) should dot-source `.env.staging` instead of requiring manual `export` before execution
3. **HIGH:** Sales Ops `lib/env.ts` must add `TRUEVOW_WEBHOOK_SECRET_SALES_OPS` to its Zod schema before cross-repo integration tests can use it
4. **HIGH:** `SAAS_ADMIN_BASE_URL` default port mismatch — scripts default to `:3000`, `.env.staging` sets `:3001`, SaaS Admin `.env.local` sets `SAAS_ADMINISTRATION_SERVICE_PORT=3001`
5. **MEDIUM:** Create a separate staging Supabase project for Gate 1 to avoid polluting development data
6. **MEDIUM:** Deploy a staging instance of SaaS Admin (either local Docker or Fly.io staging app) for live HMAC integration tests
7. **LOW:** Evaluate Infisical or similar for cross-service secret sharing between SaaS Admin and Sales Ops
