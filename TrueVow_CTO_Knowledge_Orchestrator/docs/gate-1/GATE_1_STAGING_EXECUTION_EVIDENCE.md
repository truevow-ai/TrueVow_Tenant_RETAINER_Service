# Gate 1 Staging Execution — Partial Evidence

**Date:** 2026-08-01
**Status:** RPC column mismatch discovered — SaaS Admin agent must fix

---

## Environment Verified

| Check | Status |
|---|---|
| SaaS Admin staging DB reachable (pooler us-west-1:6543) | ✅ |
| Sales Ops staging DB reachable (pooler us-east-1:6543) | ✅ |
| HMAC secret configured (64-char hex) | ✅ |
| Canonical webhook path: `/api/v1/webhooks/sales-ops/application-approved` | ✅ |
| `.env.staging` git-ignored in both repos | ✅ |
| Pooler regions corrected | ✅ |
| `fn_process_handoff()` exists in staging | ✅ |
| All required tables exist | ✅ |

## Defect Found

`fn_process_handoff()` RPC (`migration 177_transactional_handoff_rpc.sql`) references stale column names:

| RPC uses | Actual table | Actual columns |
|---|---|---|
| `customer_contacts` | Should be `core_contacts` | `full_name` not `contact_name`, `company` not `firm_name`, `source_lead_id` not `sales_lead_id`, no `role`/`is_primary` columns |
| `core_tenants` | Should be `tenant_accounts` | 585 existing rows vs 7 in `core_tenants` |

The RPC was partially fixed (`customer_contacts` → `core_contacts` columns aligned) but the function re-creation failed due to a parameter signature mismatch with the old version.

## Next Step

SaaS Admin agent must:
1. Drop old `fn_process_handoff()` with all signatures
2. Fix all column references in the RPC to match actual staging schema
3. Re-create RPC against staging
4. Verify with a test handoff call
5. Re-run `staging-failure-injection.js`
