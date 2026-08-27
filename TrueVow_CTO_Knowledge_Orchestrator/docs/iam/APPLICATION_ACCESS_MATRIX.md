# Application Access Matrix — IAM-G0

| Service | Clerk App | Auth method | Has middleware | Has sign-in UI | Has RBAC tables | Has RLS |
|---|---|---|---|---|---|---|
| SaaS Admin | App 1 | `@clerk/nextjs` full | Yes | Yes | Yes (tenant_roles, tenant_users) | Yes |
| Sales Ops | App 2 | `@clerk/nextjs` full | Yes | Yes | No | Minimal |
| CS Support Core | App 1 | `@clerk/nextjs` full | Yes | Yes | Yes (cs_team_members) | Yes |
| First-Line Support | App 2 | `@clerk/nextjs` full | Yes | Yes | Yes (cs_team_members) | Yes |
| Customer Portal | App 3 | `@clerk/nextjs` full + `clerkClient()` | Yes | Yes | No | Yes |
| Billing Service | App 3 | `@clerk/nextjs` light | Yes | Yes | No | No |
| INTAKE (Python) | App 3 | Clerk JWT only | Yes (Python) | No | Yes (user_roles) | Yes |
| RETAINER (Python) | App 3 | Clerk JWT only | Yes (Python) | No | No | Yes |
| TRACE (Python) | App 3 | Clerk JWT only | Yes (Python) | No | No | Yes |
| SETTLE | N/A | None | No | No | No | No |
| VERIFY | N/A | None | No | No | No | No |
| COMMAND | N/A | None | No | No | No | No |
| LEVERAGE | N/A | None | No | No | No | No |
| Platform Analytics | N/A | None | No | No | No | No |
| Communications | N/A | None | No | No | No | Minimal |
| Internal Ops | N/A | Supabase (data only) | No | No | No | No |
| Financial Mgmt | N/A | Supabase (data only) | No | No | No | Yes |
| 2026 Website | N/A | None | No | No | No | No |

## Cross-Application Access

**Current state:** Clerk session from App 3 (Tenants) is NOT valid for App 1 or App 2. Cross-domain auth uses `@truevow/auth-client` `CrossDomainExchange`. Staff impersonation in Customer Portal requires explicit scoped token exchange. No shared session between Clerk apps.

**Gap:** No `application_access_grants` table exists. Access is determined by: which Clerk app you authenticate against + which service's middleware you pass + what RBAC tables exist in that service's database.
