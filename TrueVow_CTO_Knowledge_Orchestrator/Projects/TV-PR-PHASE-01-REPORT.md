# TV-PR-PHASE-01 — Evidence Report

**RESULT: PARTIAL — 4/5 healthy**

---

## 1. Executive Result

```
PHASE: TV-PR-PHASE-01
RESULT: PARTIAL
CORE SERVICES HEALTHY: 4/5
```

## 2. Service Matrix

| Service | Expected Commit | Deployed Commit | API | Worker | Dependencies | Result |
|---------|----------------|-----------------|-----|--------|-------------|--------|
| FM | 3f587e5 | 3673bca (+ops) | ✅ 200 | N/A | DB | HEALTHY |
| INTAKE | 57f05ae | 9745449 | ⚠️ 200 degraded | — | DB disconnected | DEGRADED |
| SaaS Admin | 1cb75ba | 1cb75ba | ✅ 200 | — | DB | HEALTHY |
| Billing | 6da54b6 | 50c831f (+ops) | ❌ timeout | ❌ | DB unreachable | BLOCKED |
| Sales Ops | 7647de2 | 7b7d1d9 (+fixes) | ✅ 200 | ✅ | build/runtime | HEALTHY |

## 3. Billing Evidence

- **Commit**: 50c831f (ops-only descendant of 6da54b6)
- **Fly config**: `[http_service]` on port 8000, Python 3.13-slim, matching FM's working pattern
- **Secrets**: DATABASE_URL and Clerk keys set
- **Machine state**: Started, 0/1 health checks
- **Root cause**: App startup hangs at `init_billing_database()` — DB unreachable from Fly IPv6 network
- **Classification**: INFRA_DATABASE — Supabase pooler not reachable from Fly's ewr region

## 4. Sales Ops Evidence

- **Commit**: 7b7d1d9 (build-fix descendant of 7647de2)
- **Build passes**: npm install → npm run build → Docker build → Fly deploy
- **Fixes applied**: Duplicate import removed, orphaned syntax fixed, @supabase/ssr added, force-dynamic layout, Dockerfile data/migrations skip
- **Health**: `GET /api/health` → 200 `{"status":"healthy"}`
- **Nodes**: Deployed on Fly ewr region

## 5. Changes Made

| Repo | File | Reason | Classification |
|------|------|--------|---------------|
| Billing | Dockerfile | Python 3.13, shell CMD, slim base | ops |
| Billing | fly.toml | http_service config matching FM | ops |
| Sales Ops | lib/supabase-server.ts | Remove orphaned syntax | bugfix |
| Sales Ops | lib/services/lead-promotion-service.ts | Remove duplicate import | bugfix |
| Sales Ops | package.json | Add @supabase/ssr dep | bugfix |
| Sales Ops | app/layout.tsx | force-dynamic to skip SSR at build | build-fix |
| Sales Ops | Dockerfile | Auth mock, data dir creation | ops |
| Sales Ops | .dockerignore | Exclude applied migrations | ops |

No application behavior changes beyond build fixes.

## 6. Defects

| ID | Classification | Service | Detail |
|----|---------------|---------|--------|
| D-01 | INFRA_DATABASE | Billing | Supabase pooler unreachable from Fly ewr. App startup hangs at DB init. |
| D-02 | INFRA_DATABASE | INTAKE | DB status "disconnected". Pooler URL may need update. |

## 7. Security

- No secret values in report
- No real customer data used
- No real invoice or payment created
- Billing in BILLING_LEGACY mode

## 8. Gate

**NOT_READY_FOR_PHASE_02** — Billing requires database connectivity resolution.
