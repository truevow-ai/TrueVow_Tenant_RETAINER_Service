# IAM Target Architecture — IAM-G1

**Frozen:** 2026-08-02
**Version:** 1.0.0

---

## Architecture Decision

Supabase Auth is the sole human identity provider. Clerk is removed. PostgreSQL remains authoritative for memberships, roles, permissions, application access, and tenant isolation. Machine-to-machine routes use HMAC or scoped service credentials.

## Authority Boundaries

```
Human authentication         → Supabase Auth (auth.users)
Identity profile authority   → SaaS Admin Identity Core (identity_profiles)
Tenant authority             → SaaS Admin (tenant_accounts)
Platform membership          → SaaS Admin Identity Core (platform_staff_memberships)
Law-firm membership          → SaaS Admin Identity Core (tenant_memberships)
Client portal membership     → SaaS Admin Identity Core (client_portal_memberships)
Roles and permissions        → PostgreSQL RBAC tables
Application access           → application_access_grants
Tenant data enforcement      → PostgreSQL RLS
Machine-to-machine auth      → HMAC (WebhookSignature v1.0) or scoped service credentials
External webhooks            → Provider-specific signature verification
DB administrative access     → Server-only scoped database credentials
```

## Trust Domains

| Domain | Auth | Services |
|---|---|---|
| Platform Operators | Supabase Auth (JWT → identity_profiles → platform_staff_memberships) | SaaS Admin, CSM Core, Internal Ops, Financial Mgmt, Billing |
| Sales & Support | Supabase Auth (JWT → identity_profiles → platform_staff_memberships with app=sales-ops) | Sales Ops |
| Tenants | Supabase Auth (JWT → identity_profiles → tenant_memberships) | INTAKE, Customer Portal, TRACE, SETTLE, LEVERAGE, VERIFY |

## JWT Validation Pattern

**Pattern A (Backend-mediated)** — recommended for all privileged operations:
```
Browser → Supabase Auth JWT → product backend validates via JWKS → checks local iam_access_projection → performs scoped DB operation
```

**Pattern B (Direct Supabase Data API)** — requires proof of: issuer validation, audience validation, subject propagation, role handling, RLS enforcement, key rotation, revocation behavior, cross-project isolation. Not approved yet.

## Cross-Service Authorization

SaaS Admin Identity Core publishes identity/access changes through `mdm_events_outbox`. Each product maintains a local `iam_access_projection` containing only what it needs: `identity_id`, `application_code`, `tenant_id`, `membership_status`, `role_codes`, `permission_codes`, `authorization_version`, `updated_at`.

Products must not independently mutate canonical identity or membership records.
