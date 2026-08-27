# IAM Migration Inventory — RETAINER Service

**Migration:** Clerk Auth → Supabase Auth (via truevow_auth)
**Date:** 2026-08-03
**Service:** TrueVow RETAINER (Python FastAPI)
**Repo:** TrueVow_Tenant_RETAINER_Service

## Topology

```
Before:
  User/JWT → RETAINER → clerk.py (PyJWKClient) → Clerk JWKS (RS256)

After:
  User/JWT → RETAINER → clerk.py (truevow_auth) → Supabase JWKS (RS256)
```

## Files Changed

| File | Change | Status |
|------|--------|--------|
| `app/auth/clerk.py` | Rewrite — `truevow_auth.verify_supabase_jwt()` | DONE |
| `app/core/config.py` | Replace `clerk_*` → `supabase_*` config fields | DONE |
| `app/main.py` | Docstring update, lifespan enforcement, `configure()` | DONE |
| `.env.example` | Replace Clerk env vars → Supabase | DONE |
| `docs/iam/IAM_MIGRATION_INVENTORY.md` | This report | DONE |
| `docs/iam/IAM_CLERK_ZERO_REFERENCE_REPORT.md` | Zero-reference audit | DONE |

## Dependency Changes

| Dependency | Before | After | Notes |
|-----------|--------|-------|-------|
| `pyjwt[crypto]` | >=2.9.0 | >=2.9.0 | Already present — no change |
| `truevow_auth` | Not used | Required | Shared library at `shared-libraries/auth/python/truevow_auth/` |
| PyJWKClient import | `app/auth/clerk.py` | Removed — now in `truevow_auth` | Canonical single source |

## Environment Variables

| Removed | Added | Notes |
|---------|-------|-------|
| `CLERK_JWKS_URL` | `SUPABASE_JWKS_URL` | Supabase project JWKS endpoint |
| `CLERK_ISSUER` | `SUPABASE_JWT_ISSUER` | e.g. `https://<project>.supabase.co/auth/v1` |
| `CLERK_AUDIENCE` | (hardcoded) | `"authenticated"` — Supabase convention |
| `CLERK_JWKS_CACHE_TTL` | (removed) | `truevow_auth` manages its own cache |

## Auth Mode Behavior

| AUTH_MODE | Behavior | Environment |
|-----------|----------|-------------|
| `local` | HS256 local secret | development, testing |
| `supabase` | RS256 via Supabase JWKS + truevow_auth | production |

**Fail-closed:** If `AUTH_MODE=supabase` and `SUPABASE_JWKS_URL` is unset or unreachable, authentication fails. No Clerk fallback exists.

## Interface Compatibility

| Interface | Impact | Notes |
|-----------|--------|-------|
| `GET /health` | None | No auth required |
| `GET /ready` | None | No auth required |
| `POST /api/v1/retainer/*` (user) | JWT issuer/audience change | Claims mapping unchanged (`sub`, `org_id`/`firm_id`, `role`) |
| `POST /api/v1/retainer/webhooks/*` | None | HMAC WebhookSignature v1.0 — unchanged |
| Outbox events | None | No auth in payload |

## Frozen Contracts

No frozen contracts were modified. The JWT verification is internal to the RETAINER service. Cross-service communication uses HMAC WebhookSignature v1.0 which is unchanged.

## Webhook Clients Affected

None. Other services (INTAKE, SaaS Admin) communicate with RETAINER via HMAC-signed webhooks, not JWTs. The `get_webhook_context` dependency in `app/auth/deps.py` is untouched.
