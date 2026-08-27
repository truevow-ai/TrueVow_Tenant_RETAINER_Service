# Identity Table Register — IAM-G0

| Table | Service | Purpose | RLS |
|---|---|---|---|
| `tenant_roles` | SaaS Admin (migration 116) | Role definitions per tenant | `tenant_roles_isolation` |
| `tenant_users` | SaaS Admin (migration 116) | User-to-tenant memberships | `tenant_users_isolation` |
| `tenant_user_roles` | SaaS Admin (migration 116) | Role assignments (junction) | — |
| `system_admin_users` | SaaS Admin (migration 004) | Platform admin users | — |
| `user_roles` | INTAKE | RBAC with JSONB permissions | `USING (tenant_id = ...)` |
| `users` | INTAKE (`supabase_schema.sql:35`) | Email, firm_id, role, product_access | — |
| `cs_team_members` | CS Support Core + First-Line Support | Contains `clerk_user_id`, role, department | — |
| `firm_staff` | INTAKE (`001_create_growth_tier_tables.sql:86`) | Non-attorney staff with JSONB permissions | — |
| `tenant_permissions` (FDW) | INTAKE (archived) | Foreign data wrapper to Internal Ops | — |

**Missing (not found in any migration):**
- `auth.users` — no Supabase Auth users table
- `identity_profiles` — proposed in IAM plan, not yet created
- `tenant_memberships` — reliance on Clerk org_id instead
- `platform_staff_memberships` — uses `system_admin_users` and `cs_team_members` separately
- `client_portal_memberships` — not modeled
- `application_access_grants` — not modeled
- `authority_grants` — not modeled
- `identity_audit_events` — not modeled
