# PLATFORM-E2E-00A — Final Status

> **Date**: 2026-08-04
> **Status**: 3/5 deployed and healthy. 2 packaging-complete with build env blockers.

---

## Deployed and Healthy (3/5)

| Service | App | Health | Commit |
|---------|-----|--------|--------|
| **INTAKE** | truevow-tenant-public | ✅ | 9745449 |
| **SaaS Admin** | truevow-saas-admin-staging | ✅ | 1cb75ba |
| **FM** | truevow-fm-staging | ✅ `GET /health` → 200 | 3673bca |

## Packaging Complete, Build-Blocked (2/5)

| Service | App | Commit | Blocker |
|---------|-----|--------|---------|
| **Billing** | truevow-billing-staging | 0ff563d | Deploys, machine starts, health check fails. Needs Redis + IPv4 connectivity. Secrets configured. |
| **Sales Ops** | truevow-sales-ops | 963e5ae | Dockerfile + .dockerignore correct. Build works on Linux. Windows reparse points break Fly remote builder. `npm run build` is CPU-intensive, needs build env with 4GB+ memory. |

---

## DB / Migrations Complete

```
INTAKE: PI_STANDARD_INTAKE v1.0.0 seeded, checksum MATCH
SaaS Admin: Migrations 185-187 applied
FM: Migration chain 012-014 applied, inbox constraints active
```

---

## Sales Ops Diagnosis

Root causes found and fixed:
1. `jose` missing — mock `@truevow/auth` now includes `jose` dep
2. `supabase/migrations/_applied/` excluded from context
3. Windows reparse points (Next.js route dirs like `[id]`) cause `archive/tar: unknown file mode ?rwxr-xr-x` on Fly remote builder — build from Linux env

## Billing Diagnosis

Dockerfile + fly.toml correct. App deploys, machine starts, but health check fails because:
1. Container is IPv6-only (Fly), DB is at Supabase (requires IPv4)
2. Redis not available (app requires Redis for idempotency + arq worker)
3. Needs `shared-cpu-1x` + dedicated IPv4 in Fly config

## Next: Configure Billing Fly networking, build Sales Ops on Linux, then HMAC commissioning
