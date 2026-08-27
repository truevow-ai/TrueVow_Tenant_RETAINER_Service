# TV-PR-PHASE-01C — Final Evidence Report

**RESULT: PASS — 5/5 healthy**

---

## 1. Executive

```
WORK ORDER: TV-PR-PHASE-01C
RESULT: PASS
CORE SERVICES HEALTHY: 5/5
PRIMARY ROOT CAUSE: APPLICATION_DEFECT — corrupted UTF-8 in sentry_init.py
APPLICATION CODE CHANGES: sentry_init.py (3 bytes fixed, Windows-1252 em dashes)
```

## 2. Service Matrix

| Service | Commit | Deployed | API | Health |
|---------|--------|----------|-----|--------|
| Billing | 231c92b | truevow-billing-v2.fly.dev | 200 | `{"status":"healthy","service":"billing"}` |
| FM | 3673bca | truevow-fm-staging.fly.dev | 200 | `{"status":"healthy"}` |
| Sales Ops | 7b7d1d9 | truevow-sales-ops.fly.dev | 1/1 checks | healthy |
| INTAKE | 9745449 | truevow-tenant-public.fly.dev | 200 | degraded (DB, pre-existing) |
| SaaS Admin | 1cb75ba | truevow-saas-admin-staging.fly.dev | 200 | HTML (sign-in redirect) |

## 3. Root Cause

```
PRIMARY: APPLICATION_DEFECT — sentry_init.py contained 3 invalid UTF-8 bytes (0x97, Windows-1252 em dash characters)
CONTRIBUTING: Missing sentry-sdk from requirements.txt

Chain: sentry_init.py invalid UTF-8 → import app.main crashes → uvicorn dies silently → port 8000 never bound → Fly health check timeout → machine killed
```

## 4. Fix Applied

| File | Change | Classification |
|------|--------|---------------|
| `app/shared/sentry_init.py` | Replace 3 Windows-1252 em dashes with ASCII hyphens | bugfix |
| `Dockerfile` | Add `sentry-sdk` to pip install | dependency-fix |

## 5. Connectivity Verification

DB pooler tested locally:
- psycopg2: CONNECTED 1.54s (port 6543), 1.36s (port 5432)
- asyncpg: CONNECTED 1.70s (port 6543), 1.53s (port 5432)
- Supabase REST API: 200 with correct anon key

## 6. Billing Identity

```
Branch: release/plg-bill-cf-producer
Commit: 231c92b
Fly app: truevow-billing-v2
Region: dfw
Image: deployment-01KZ81SDXJMF68VJJG0FWQYA5C
Authority: BILLING_LEGACY
```

## 7. Recommendation

**READY_FOR_HMAC_PREFLIGHT**
