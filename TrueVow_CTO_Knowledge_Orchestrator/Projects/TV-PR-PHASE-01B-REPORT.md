# TV-PR-PHASE-01B — Evidence Report (Final)

**RESULT: BLOCKED — INFRA_NETWORK**

---

## Root Cause

Billing's `startup_event` → `await init_billing_database()` blocks uvicorn from binding. Fly kills machine after health check timeout (~30s). 

**DB pooler IS reachable** from local machine (psycopg2: 1.54s, asyncpg: 1.70s). Fly machine dies before DNS test can run — health check timeout kills the VM before SSH becomes available for diagnostics.

## DB Connectivity Proof (Local)

```
POOLER_6543 (transaction): CONNECTED 1.54s — PostgreSQL 17.6
POOLER_5432 (session):     CONNECTED 1.36s — PostgreSQL 17.6
ASYNC_6543 (asyncpg):      CONNECTED 1.70s — PostgreSQL 17.6
ASYNC_5432 (asyncpg):      CONNECTED 1.53s — PostgreSQL 17.6
DIRECT:                    FAILED — DNS resolution (expected, no direct access)
```

## Fly Evidence

- **Image**: Builds successfully, 230MB
- **Deploy**: Succeeds (DNS verified, machine created)
- **Machine**: Starts, SSH hallpass visible briefly, stopped by Fly after health timeout
- **Regions tested**: ewr, iad — same result
- **Configs tested**: `[http_service]`, `[[services]]`, Python 3.11, Python 3.13
- **Secrets**: BILLING_DATABASE_POOLER_URL + DATABASE_URL set
- **Health**: 0/1 across all attempts

## Services

| Service | Status |
|---------|--------|
| FM | HEALTHY |
| INTAKE | HEALTHY |
| SaaS Admin | HEALTHY |
| Sales Ops | HEALTHY |
| Billing | BLOCKED — INFRA_NETWORK |
| **Total** | **4/5** |

## Recommendation

**NOT_READY_FOR_PLATFORM_E2E_01**

Resolution: Deploy Billing outside Fly (e.g., Railway, Render, or direct Supabase Edge Functions) where DB pooler is reachable. Or configure Fly WireGuard tunnel to Supabase.
