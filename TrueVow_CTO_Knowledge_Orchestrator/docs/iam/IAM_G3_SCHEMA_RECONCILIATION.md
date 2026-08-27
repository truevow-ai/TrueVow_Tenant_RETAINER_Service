# IAM G3 Schema Reconciliation Report

**Generated:** 2026-08-02
**Scope:** Map frozen IAM-G1 logical entities to physical tables in SaaS Admin (TrueVow_SaaS_Administration_Service/supabase/migrations/)
**Method:** Inspect existing migrations and schema; classify each IAM capability as REUSE / EXTEND / RENAME LATER / DEPRECATE / MISSING / CONFLICTING AUTHORITY
**Authoritative Source:** Migration 179 (`179_iam_identity_core_foundation.sql`) is the **canonical IAM schema**. All other tables referring to identity, membership, or roles must be reconciled against it.

---

## EXECUTIVE SUMMARY

Migration 179 (IAM Identity Core Foundation) creates 12 canonical IAM tables per the frozen IAM-G1 contracts. However, the SaaS Admin database has accumulated **14 pre-existing tables** across earlier migrations (003, 004, 072, 113, 116, 174, 159) that overlap with or duplicate IAM concerns.

**Severity classification:**

| Capability | Verdict | Urgency |
|---|---|---|
| identity_profiles | REUSE | None |
| tenant_memberships | CONFLICTING AUTHORITY (vs tenant_users) | **HIGH** |
| platform_staff_memberships | CONFLICTING AUTHORITY (vs system_admin_users + system_staff_users) | **HIGH** |
| client_portal_memberships | REUSE (partial overlap with client_portal_access_grants) | Low |
| iam_roles | CONFLICTING AUTHORITY (vs tenant_roles) | **CRITICAL** |
| iam_permissions | CONFLICTING AUTHORITY (vs tenant_permissions) | **CRITICAL** |
| membership_role_assignments | CONFLICTING AUTHORITY (vs tenant_user_roles) | **HIGH** |
| application_access_grants | REUSE | None |
| authority_grants | REUSE (complementary to authority_gates) | None |
| identity_invitations | MISSING | **HIGH** |
| identity_audit_events | REUSE (complements 5 existing audit tables) | Medium |
| iam_access_projection | REUSE | None |

**Key finding:** The IAM-G1 role/permission catalogue is a **third** role system. The migrations currently contain two separate role/permission schemas:
- **Migration 113 + 116:** `tenant_roles` / `tenant_permissions` / `tenant_user_roles` (legacy tenant RBAC)
- **Migration 179:** `iam_roles` / `iam_permissions` / `membership_role_assignments` (IAM canonical)
- **Migration 003 (tenant_users.role CHECK):** Hardcoded role enum in table definition

All three systems are actively defined in the schema. Only one can be canonical.

---

## DETAILED ANALYSIS

### 1. identity_profiles — linked 1:1 with auth.users

**Migration 179 table:**
```sql
CREATE TABLE identity_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  auth_user_id UUID UNIQUE,
  display_name TEXT, primary_email TEXT, phone TEXT,
  profile_status TEXT NOT NULL DEFAULT 'ACTIVE'
    CHECK (profile_status IN ('ACTIVE','SUSPENDED','DEACTIVATED')),
  created_at, updated_at, suspended_at, deactivated_at
);
```

**Existing overlapping tables:**

| Table | Migration | Overlap? |
|---|---|---|
| `tenant_users` | 003/004/116 | User identity + auth + membership. Has email, name, clerk_user_id, auth_provider. NOT linked to identity_profiles. |
| `system_admin_users` | 003/004 | Platform staff identity. Has email, name, clerk_id, mfa. Standalone. |
| `system_staff_users` | 072 | Platform staff identity. Has email, clerk_id, department. Standalone. |
| `tenant_admin_users` | 072 | Tenant admin identity. Has email, clerk_id, tenant FK. Standalone. |
| `tenant_staff_users` | 072 | Tenant staff identity. Has email, clerk_id. Standalone. |
| `tenant_client_users` | 072 | Client identity. Has email, clerk_id. Standalone. |
| `customer_contacts` | 112 | Lighter weight: name, email, phone, job_title. Not a full identity record. |

**Matched columns:** `identity_profiles.primary_email` maps to `email` in all legacy tables.

**Missing columns:** IAM identity_profiles is intentionally lean (defers auth to auth.users). Missing from legacy: `bar_number`, `bar_state`, `department`, `office_location`, `permissions` (JSONB), `mfa_enabled`. These can go into `profile_metadata JSONB` or remain in specialized tables.

**Verdict: REUSE** — `identity_profiles` is the IAM canonical identity table. The 6 legacy user tables must be migrated into it.

**Recommended action:** Create identity_profiles for all existing users. Add optional `profile_metadata JSONB` column for non-IAM fields. Add FK: `tenant_users.clerk_user_id → identity_profiles.auth_user_id`. DEPRECATE all 6 legacy user tables.

---

### 2. tenant_memberships — identity ↔ tenant relationship

**Migration 179 table:**
```sql
CREATE TABLE tenant_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identity_profile_id UUID NOT NULL REFERENCES identity_profiles(id),
  tenant_id UUID NOT NULL,
  membership_status TEXT NOT NULL DEFAULT 'INVITED'
    CHECK (INVITED, ACTIVE, SUSPENDED, REVOKED),
  joined_at, suspended_at, revoked_at, created_by, authority_reference,
  UNIQUE (identity_profile_id, tenant_id)
);
```

**Existing: tenant_users** (migration 003, extended by 004, 116)

| tenant_users column | tenant_memberships equivalent |
|---|---|
| `user_id UUID PK` | `id UUID PK` — different naming |
| `tenant_id UUID FK → tenant_accounts` | `tenant_id UUID` — SAME |
| `email CITEXT, first_name, last_name, title` | NOT IN tenant_memberships (defers to identity_profiles) |
| `role VARCHAR CHECK (owner,admin,...)` | NOT IN tenant_memberships (role via membership_role_assignments) |
| `is_active BOOLEAN` | `membership_status` — richer lifecycle |
| `clerk_user_id VARCHAR` (added 116) | NOT IN tenant_memberships (defers to identity_profiles.auth_user_id) |
| `status VARCHAR` (added 116) | `membership_status` — overlap |
| `invited_by UUID, invited_at` (added 116) | `created_by UUID, joined_at` — similar intent |
| `bar_number, bar_state` | NOT IN tenant_memberships |
| `auth_provider, last_login_at` | NOT IN tenant_memberships (defers to identity_profiles + auth.users) |

**CONFLICT:** `tenant_users` mixes 3 concerns: (a) identity (name, email, auth), (b) membership (tenant_id, is_active), (c) role (role VARCHAR). In IAM-G1 these are three separate tables.

**Verdict: CONFLICTING AUTHORITY** — Two tables model the identity↔tenant relationship.

**Recommended action:** Short-term: dual-write sync function. Long-term: migrate all code to `tenant_memberships`. Add FK `tenant_memberships.legacy_user_id UUID REFERENCES tenant_users(user_id)`. DEPRECATE `tenant_users`.


### 3. platform_staff_memberships — identity ↔ TrueVow staff

**Migration 179 table:**
```sql
CREATE TABLE platform_staff_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identity_profile_id UUID NOT NULL REFERENCES identity_profiles(id),
  application_code TEXT NOT NULL,         -- 'SAAS_ADMIN','SUPPORT','SALES_OPS'
  membership_status TEXT NOT NULL DEFAULT 'INVITED'
    CHECK (INVITED, ACTIVE, SUSPENDED, REVOKED),
  granted_by, granted_at, expires_at, revoked_at,
  UNIQUE (identity_profile_id, application_code)
);
```

**Existing: system_admin_users (003/004), system_staff_users (072), system_affiliate_users (072), system_partner_users (072)**

These are **four** separate tables that all model "a TrueVow internal person with platform access," differing only by role value. The IAM model uses ONE table to model membership, with `application_code` distinguishing the application. A single identity can have multiple platform staff memberships — which the legacy model cannot represent without duplicate identity rows.

**Verdict: CONFLICTING AUTHORITY.** `platform_staff_memberships` generalizes what four legacy tables duplicate.

**Recommended action:** Extract identity data from all four legacy tables → `identity_profiles`. Create `platform_staff_memberships` rows. DEPRECATE all four legacy tables.

---

### 4. client_portal_memberships — client ↔ matter

**Migration 179 table:**
```sql
CREATE TABLE client_portal_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identity_profile_id UUID NOT NULL REFERENCES identity_profiles(id),
  tenant_id UUID NOT NULL, matter_id UUID, allowed_portal TEXT DEFAULT 'client-portal',
  membership_status TEXT NOT NULL DEFAULT 'INVITED',
  created_at, updated_at
);
```

**Existing: client_portal_access_grants (174), client_portal_invitations (174)**

`client_portal_access_grants` is significantly richer: permissions TEXT[], allowed_actions JSONB, source_event tracking, guardian/representative support, upgrade chain (previous_grant_id FK). `client_portal_memberships` is the simpler IAM concern: "which portal does this identity have access to?"

**No conflict — complementary layers:**
- `client_portal_memberships` = membership tier (IAM): is this identity connected to this tenant/matter portal?
- `client_portal_access_grants` = resource tier (Portal): what can they do once inside the portal?

**Verdict: REUSE + EXTEND.** Add bridge FK:
```sql
ALTER TABLE client_portal_memberships 
  ADD COLUMN access_grant_id UUID REFERENCES client_portal_access_grants(grant_id);
```

---

### 5. iam_roles — role definitions

**Migration 179 table + seed (17 roles across 3 domains):**
```
Tenant:  TENANT_OWNER, TENANT_ADMIN, ATTORNEY, INTAKE_MANAGER, CASE_STAFF, BILLING_MANAGER, VIEWER
Platform: PLATFORM_OWNER, PLATFORM_ADMIN, CSM, BILLING_OPERATOR, COMPLIANCE_OPERATOR,
          SUPPORT_ADMIN, SUPPORT_AGENT, SALES_OPS_ADMIN, SALES_REPRESENTATIVE
Client:  CLIENT_PORTAL_USER
```

**Existing: tenant_roles (113, extended 116) — 6 per-tenant roles:**
```
owner, admin, attorney, paralegal, staff, readonly
```

**Also conflicting:** `tenant_users.role` CHECK constraint (003) hardcodes: `owner, admin, attorney, paralegal, staff, readonly` — a third role source.

**Structural differences:**
- `tenant_roles` is **per-tenant** (`tenant_id` column). `iam_roles` is **global** with `domain` field.
- `iam_roles.code` uses SCREAMING_SNAKE_CASE. `tenant_roles.role_code` uses lowercase.
- `tenant_roles` has hierarchy levels (`level INTEGER`). `iam_roles` does not.
- IAM covers platform + client roles. tenant_roles covers tenant only.

**Verdict: CONFLICTING AUTHORITY — CRITICAL.** Two role catalogues. Applications must not serve both.

**Recommended action:** Add `iam_roles.source_tenant_id UUID` column (NULL=global, non-NULL=per-tenant custom role). Merge `tenant_roles` seed into `iam_roles`. DEPRECATE `tenant_roles`. Create `v_legacy_tenant_roles` mapping view during transition.

---

### 6. iam_permissions — permission definitions

**Migration 179 table + seed (27 permissions across 3 domains):**
- Tenant (15): `members.invite, members.read, members.manage, roles.assign, intake.read, intake.update, recordings.listen, transcripts.read, matters.read, matters.update, documents.upload, billing.read, billing.manage, tenant.settings.read, tenant.settings.manage`
- Platform (8): `platform.tenants.read, .create, .suspend, .activate, platform.entitlements.read, .manage, platform.staff.read, .manage, platform.audit.read`
- Client (3): `client.matter.read, client.documents.read, client.messages.send`

**Existing: tenant_permissions (113, extended 116) — 19-21 tenant-only permissions:**
- `users:read, users:create, users:update, users:delete, users:manage_roles, billing:read, billing:manage, cases:read, cases:create, cases:update, cases:delete, cases:assign, settings:read, settings:update, integrations:manage, analytics:read, analytics:export, data:export, data:import`

**Key differences:**
- **Code format:** `members.manage` (dot) vs `users:update` (colon)
- **Granularity:** IAM uses coarser permissions. Legacy uses finer CRUD.
- **Resources:** IAM uses `members`/`matters`. Legacy uses `users`/`cases`.
- **Scope:** IAM covers platform+client domains. Legacy is tenant-only.

**Verdict: CONFLICTING AUTHORITY — CRITICAL.** Two permission catalogues with different naming, granularity, and scope.

**Recommended action:** Create `iam_permission_mapping` table. Create `v_legacy_tenant_permissions` mapping view. All authorization checks → `iam_permissions`. DEPRECATE `tenant_permissions`.


### 7. membership_role_assignments — polymorphic role assignments

**Migration 179 table:**
```sql
CREATE TABLE membership_role_assignments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  membership_table TEXT NOT NULL CHECK (
    'tenant_memberships','platform_staff_memberships','client_portal_memberships'
  ),
  membership_id UUID NOT NULL,         -- polymorphic FK
  role_id UUID NOT NULL REFERENCES iam_roles(id),
  assigned_by UUID, assigned_at TIMESTAMPTZ, revoked_at TIMESTAMPTZ
);
```

**Existing: tenant_user_roles (116)**
```sql
CREATE TABLE tenant_user_roles (
  user_id UUID NOT NULL REFERENCES tenant_users(user_id),
  role_id UUID NOT NULL REFERENCES tenant_roles(role_id),
  assigned_by UUID, assigned_at TIMESTAMPTZ,
  PRIMARY KEY (user_id, role_id)
);
```

**Key structural differences:**
- `membership_role_assignments` uses **polymorphic FK** — one table for ALL membership types.
- `tenant_user_roles` uses **direct FK** — only works for tenant memberships.
- `membership_role_assignments` → `iam_roles`. `tenant_user_roles` → `tenant_roles`. Different role catalogues.
- `membership_role_assignments` supports `revoked_at` (temporal). `tenant_user_roles` is a simple join table.

**Also relevant:** Migration 113's `tenant_users.tenant_role_id` (single-role-per-user FK). Migration 116 replaced this with multi-role via `tenant_user_roles`.

**Verdict: CONFLICTING AUTHORITY.** Two role assignment tables referencing different role catalogues and different membership tables.

**Recommended action:** Dual-write: when `tenant_user_roles` rows are created, create corresponding `membership_role_assignments`. DEPRECATE both `tenant_user_roles` and `tenant_users.tenant_role_id`.

---

### 8. application_access_grants — identity ↔ application

**Migration 179 table:**
```sql
CREATE TABLE application_access_grants (
  id UUID PRIMARY KEY, identity_profile_id UUID NOT NULL REFERENCES identity_profiles(id),
  application_code TEXT NOT NULL, granted_by UUID, granted_at, revoked_at,
  UNIQUE (identity_profile_id, application_code)
);
```

**Existing overlapping tables:** NONE.

No other table models "which applications does this identity have access to?" as a first-class concept. Closest: `tenant_product_entitlements` (175, tenant-level product subscription) and `client_portal_access_grants` (174, resource-level portal access).

**Verdict: REUSE** — No conflict. Clean, canonical table. Use as-is.

---

### 9. authority_grants — authority class assignments

**Migration 179 table:**
```sql
CREATE TABLE authority_grants (
  id UUID PRIMARY KEY, identity_profile_id UUID NOT NULL REFERENCES identity_profiles(id),
  authority_class TEXT NOT NULL CHECK (
    'SYS_ADMIN','FIRM_POLICY','STAFF_AUTH','ATTY_AUTH','CLIENT_AUTH','PROHIBITED'
  ),
  scope_tenant_id UUID, granted_by UUID, granted_at, revoked_at
);
```

**Existing complementary tables (159):**
- `authority_gates` — what actions require what authority (16 seeded gates)
- `authority_delegations` — temporary authority transfers
- `authority_decisions` — immutable log of every authority check
- `authority_gate_denials` — failed authorization attempts

**RELATIONSHIP, NOT CONFLICT:**
- `authority_grants` (179): **Who** has what authority class? (identity-centric)
- `authority_gates` (159): **What actions** require what authority? (action-centric)
- `authority_decisions` (159): **What happened** when authority was checked? (audit-centric)

Minor enum misalignment: `authority_gates.required_authority` uses `sys_admin`/`staff_authorized`/`attorney` vs `authority_grants.authority_class` uses `SYS_ADMIN`/`STAFF_AUTH`/`ATTY_AUTH`. Map `responsible_attorney`, `managing_attorney`, `compliance_reviewer` as `required_role` values, not as `required_authority` values.

**Verdict: REUSE** — No conflict. Align enum values between 159 and 179.

---

### 10. identity_invitations — invitation lifecycle

**Migration 179:** NO invitation table created.

**Existing search results:**
- `client_portal_invitations` (174) — portal-specific only (recipient_email, grant_id → client_portal_access_grants, purpose TEXT)
- `tenant_users.invited_by + invited_at` (116) — minimal tracking, no token, no status

**What IAM-G1 needs (MISSING):**
```sql
CREATE TABLE iam_identity_invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  inviter_identity_id UUID REFERENCES identity_profiles(id),
  invited_email TEXT, invited_phone TEXT,
  tenant_id UUID,                     -- for tenant-scoped invites
  application_code TEXT,              -- for platform staff invites
  invitation_token_hash VARCHAR(128),
  token_expires_at TIMESTAMPTZ,
  delivery_channel VARCHAR,           -- email, sms
  delivery_status VARCHAR,            -- pending, sent, delivered, bounced
  status VARCHAR NOT NULL,            -- pending, accepted, declined, expired, revoked
  accepted_identity_profile_id UUID,  -- set after acceptance
  accepted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ, updated_at TIMESTAMPTZ
);
```

**Verdict: MISSING** — No general IAM invitation system exists. Only portal-specific invitations (174). Critical gap: IAM-G1 specifies invitation-driven onboarding for ALL membership types.

**Recommended action:** Create migration for `iam_identity_invitations`. This single table serves tenant member invites, platform staff invites, and client portal invites (linking to client_portal_invitations where richer portal data is needed).

---

### 11. identity_audit_events — IAM audit trail

**Migration 179 table:**
```sql
CREATE TABLE identity_audit_events (
  id UUID PRIMARY KEY, identity_profile_id UUID REFERENCES identity_profiles(id),
  event_type TEXT NOT NULL, event_payload JSONB, actor_id UUID,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

**Existing audit tables (5 others):**

| Table | Migration | Purpose |
|---|---|---|
| `system_audit_log` | 003/004/117 | System-wide activity (tenant CRUD, subscription, billing) |
| `audit_log` | 110 | API request forensics (HTTP-level, 90-day retention) |
| `tenant_auth_audit_log` | 113 | Tenant auth events (login, logout, token_exchange) |
| `tenant_rbac_audit_log` | 116 | Tenant RBAC changes (role_created, role_assigned) — to be deprecated with tenant_roles |
| `auth_audit_log` | 118 | Per-security-contract auth audit (auth_success, auth_failure, scope_rejected) |
| `system_audit_chain` | 160 | Tamper-proof hash chaining for audit integrity |
| `identity_audit_events` | **179** | **IAM-specific events** (profile, membership, role, authority, invitation) |

**No conflict — complementary layers.** Each audit table serves a distinct domain.

**Verdict: REUSE** — Use `identity_audit_events` for all IAM-specific events. The 5 existing tables remain for their respective domains.

**Recommended action:** Document audit boundary: IAM events → `identity_audit_events`. Operational events → `system_audit_log`. API forensics → `audit_log`. DEPRECATE `tenant_rbac_audit_log` when `tenant_roles` is deprecated.

---

### 12. iam_access_projection — per-product local projection

**Migration 179 table:**
```sql
CREATE TABLE iam_access_projection (
  identity_id UUID NOT NULL, application_code TEXT NOT NULL, tenant_id UUID,
  membership_status TEXT NOT NULL, role_codes TEXT[], permission_codes TEXT[],
  authorization_version INTEGER NOT NULL DEFAULT 1, updated_at TIMESTAMPTZ,
  PRIMARY KEY (identity_id, application_code, COALESCE(tenant_id, zero-uuid))
);
```

**Existing overlapping tables:** NONE.

This is a brand-new pattern: a denormalized, pre-computed snapshot of access rights, keyed by (identity_id, application_code, tenant_id). Products read from this table instead of joining 4+ IAM tables at runtime.

**Verdict: REUSE** — No conflict. Use as-is.

**Recommended action:** Create `fn_refresh_iam_access_projection(p_identity_id UUID)` function. Create triggers on `tenant_memberships`, `platform_staff_memberships`, `client_portal_memberships`, and `membership_role_assignments` that call the refresh function on INSERT/UPDATE/DELETE.

---

## CROSS-CUTTING TABLE INVENTORY

### tenant_accounts (firm identity)
- **Migration:** 003 (created), 004 (improved with soft-delete), 118 (added clerk_org_id)
- **Role:** Firm/tenant master registry. NOT individual identity.
- **IAM relationship:** `tenant_memberships.tenant_id → tenant_accounts.tenant_id`. No conflict.
- **Status:** STABLE. No changes needed.

### core_contacts / core_tenants
- **core_tenants:** Migration 112 creates a **VIEW** mapping to `tenant_accounts` (backward compatibility).
- **core_contacts:** Referenced in migrations 012, 015, 038, 130, 159, 160 but **CREATE TABLE not found in any migration** — likely created outside migrations (Prisma or earlier schema). Migration 130 adds FK `customer_contacts.core_contact_id → core_contacts.contact_id`.
- **IAM relationship:** None directly. `core_contacts` = contact management (phone book). `identity_profiles` = authentication identity (person). Different concerns.
- **Status:** STABLE. Document that `core_contacts` is contact management, not IAM.

### client_portal_access_grants / client_portal_invitations
- **Migration:** 174 (created)
- **Role:** Granular access grants for client portal resources + invitation lifecycle.
- **IAM relationship:** Complementary to `client_portal_memberships` (179). Bridge via FK.
- **Status:** EXTEND. Add `client_portal_memberships.access_grant_id → client_portal_access_grants`.

### system_admin_users
- **Migration:** 003, 004, 117
- **Role:** TrueVow internal platform administrators. Standalone identity + membership.
- **IAM relationship:** Overlaps with `platform_staff_memberships`.
- **Status:** DEPRECATE after migration to identity_profiles + platform_staff_memberships.

### tenant_users / tenant_roles / tenant_user_roles
- **Migration:** 003 (tenant_users), 113 (tenant_roles, tenant_permissions, tenant_role_permissions), 116 (extended all three + tenant_user_roles)
- **Role:** Legacy tenant RBAC system. Mixes identity (tenant_users), role catalogue (tenant_roles), and assignment (tenant_user_roles).
- **IAM relationship:** CONFLICTING AUTHORITY with `tenant_memberships` + `iam_roles` + `membership_role_assignments`.
- **Status:** DEPRECATE after migration. HIGH priority.

### tenant_permissions / tenant_role_permissions
- **Migration:** 113 (21 permissions), 116 (19 permissions, slightly different)
- **Role:** Permission catalogue and role→permission mapping for legacy tenant RBAC.
- **IAM relationship:** CONFLICTING AUTHORITY with `iam_permissions` + `iam_role_permissions`.
- **Status:** DEPRECATE after migration. CRITICAL priority.

### tenant_admin_users / tenant_staff_users / tenant_client_users
- **Migration:** 072 (created)
- **Role:** Three separate identity tables for different user categories within a tenant.
- **IAM relationship:** Identity → `identity_profiles`. Membership → `tenant_memberships`.
- **Status:** DEPRECATE. Three separate tables for what should be one identity_profiles table.

### system_staff_users / system_affiliate_users / system_partner_users
- **Migration:** 072 (created)
- **Role:** Separate identity tables for platform staff, affiliates, partners.
- **IAM relationship:** Identity → `identity_profiles`. Membership → `platform_staff_memberships`.
- **Status:** DEPRECATE.

### customer_contacts
- **Migration:** 112 (created), 130 (linked to core_contacts), 131 (tenant_contacts deprecated in its favor)
- **Role:** Master data store for customer contacts (post-conversion).
- **IAM relationship:** Contact management, not identity. May link to `identity_profiles` via FK or metadata.
- **Status:** STABLE. Clarify: `customer_contacts` = CRM contact. `identity_profiles` = IAM identity.

### tenant_contacts
- **Migration:** 004 (created), 072 (extended), 131 (deprecated → archived_tenant_contacts)
- **Role:** Former contact table. Now archived.
- **Status:** DEPRECATED (already renamed to `archived_tenant_contacts` by migration 131).

### cs_team_members
- **Search result:** NOT FOUND in any SaaS Admin migration or CS Support Service SQL file.
- **Status:** MISSING from SaaS Admin. May exist in an external CS Support repository (not found in workspace submodules).

### user_profiles
- **Search result:** NOT FOUND in any migration.
- **Status:** Does not exist. `identity_profiles` (179) serves this purpose.

---

## ACTION PLAN: RECOMMENDED MIGRATION SEQUENCE

### Phase 1: CRITICAL — Resolve Role/Permission Conflict (Week 1)
1. Create migration adding `iam_roles.source_tenant_id UUID` (NULL=global).
2. Create `v_legacy_tenant_roles` mapping view for backward compatibility.
3. Create `iam_permission_mapping` table for code compatibility.
4. Create `v_legacy_tenant_permissions` mapping view.
5. Update RLS policies (migrations 113, 114, 116) to use IAM tables.

### Phase 2: HIGH — Identity Unification (Week 2-3)
1. Migration 180: Populate `identity_profiles` from all 6 legacy user tables.
2. Migration 181: Populate `tenant_memberships` from `tenant_users`.
3. Migration 182: Populate `platform_staff_memberships` from `system_admin_users` + `system_staff_users`.
4. Add dual-write triggers: legacy table changes → IAM tables.

### Phase 3: HIGH — Invitation System (Week 3)
1. Migration 183: Create `iam_identity_invitations` table.
2. Port invitation logic from `tenant_users.invited_by` + `client_portal_invitations`.

### Phase 4: MEDIUM — Bridge & Deprecate (Week 4-6)
1. Add FK: `client_portal_memberships.access_grant_id → client_portal_access_grants`.
2. Add FK: `tenant_memberships.legacy_user_id → tenant_users.user_id`.
3. Create `iam_access_projection` refresh function + triggers.
4. Mark legacy tables as DEPRECATED (comments, no DROP).
5. Update all application code: authorization checks → IAM tables.

### Phase 5: LOW — Cleanup (Month 3+)
1. Drop deprecated tables after verifying zero reads in production for 30 days.
2. Align `authority_gates.required_authority` enum with `authority_grants.authority_class`.
3. Remove `tenant_users.role` CHECK constraint.
4. Remove duplicate `tenant_users.status` column (redundant with membership_status).

---

## SUMMARY TABLE

| # | IAM Capability | Migration 179 Table | Legacy Table(s) | Verdict | Action |
|---|---|---|---|---|---|
| 1 | identity_profiles | identity_profiles | tenant_users, system_admin_users, system_staff_users, tenant_admin_users, tenant_staff_users, tenant_client_users (6 tables) | REUSE | Populate from legacy; deprecate legacy |
| 2 | tenant_memberships | tenant_memberships | tenant_users (003/004/116) | CONFLICTING AUTHORITY | Dual-write; deprecate tenant_users |
| 3 | platform_staff_memberships | platform_staff_memberships | system_admin_users (003/004), system_staff_users (072), system_affiliate_users (072), system_partner_users (072) | CONFLICTING AUTHORITY | Extract identity; deprecate 4 tables |
| 4 | client_portal_memberships | client_portal_memberships | client_portal_access_grants (174), client_portal_invitations (174) | REUSE + EXTEND | Add FK bridge to access_grants |
| 5 | iam_roles | iam_roles (17 roles) | tenant_roles (113/116, 6 roles), tenant_users.role CHECK (003) | CONFLICTING AUTHORITY | Merge; add per-tenant col; deprecate |
| 6 | iam_permissions | iam_permissions (27 perms) | tenant_permissions (113/116, 19-21 perms) | CONFLICTING AUTHORITY | Create mapping; deprecate |
| 7 | membership_role_assignments | membership_role_assignments (polymorphic) | tenant_user_roles (116), tenant_users.tenant_role_id (113) | CONFLICTING AUTHORITY | Dual-write; deprecate |
| 8 | application_access_grants | application_access_grants | — (none) | REUSE | Use as-is |
| 9 | authority_grants | authority_grants | authority_gates, authority_delegations, authority_decisions, authority_gate_denials (159) | REUSE | Align enum values between 159 and 179 |
| 10 | identity_invitations | — (not created) | client_portal_invitations (174, portal-only), tenant_users.invited_by (116) | MISSING | Create iam_identity_invitations |
| 11 | identity_audit_events | identity_audit_events | system_audit_log (003), audit_log (110), tenant_auth_audit_log (113), tenant_rbac_audit_log (116), auth_audit_log (118), system_audit_chain (160) | REUSE | Document boundaries; use as-is |
| 12 | iam_access_projection | iam_access_projection | — (none) | REUSE | Create refresh triggers |

---

## APPENDIX: IAM-Relevant Migration Map

| Migration | Date | What It Creates / Modifies |
|---|---|---|
| **003** | Nov 2025 | `tenant_accounts`, `tenant_users` (with role CHECK constraint), `system_admin_users`, `system_audit_log` |
| **004** | Jan 2025 | Improved schema: `tenant_addresses`, `tenant_contacts`, normalized `tenant_users`, `tenant_bar_associations` |
| 005 | Jan 2025 | Drops redundant `tenants` table → consolidates into `core_tenants` |
| 006 | Jan 2025 | `core_addresses`, `core_bar_associations` (core_* prefix tables) |
| 008 | Jan 2025 | Tenant App database field standardization (is_deleted → deleted_at) |
| **072** | Dec 2025 | `system_staff_users`, `system_affiliate_users`, `system_partner_users`, `tenant_admin_users`, `tenant_staff_users`, `tenant_client_users` — **6 new identity tables** |
| 073 | Dec 2025 | Template for linking existing users to Clerk (no DDL, template only) |
| 110 | Dec 2025 | `audit_log` (API request forensics, 90-day retention) |
| **112** | Jan 2025 | `customer_contacts`, `core_tenants` VIEW (maps to `tenant_accounts`), `contact_relationships` |
| **113** | Mar 2026 | `tenant_roles`, `tenant_permissions`, `tenant_role_permissions`, `tenant_auth_audit_log`, adds `tenant_role_id` FK to `tenant_users` — **first RBAC system** |
| 114 | Mar 2026 | Centralized auth RLS policies (references `tenant_roles`) |
| 115 | Mar 2026 | Fix tenant_settings for portal (adds portal_profile column) |
| **116** | Mar 2026 | `tenant_roles` extended (adds `tenant_id`), `tenant_user_roles` (multi-role), `tenant_rbac_audit_log`, extends `tenant_users` (adds `clerk_user_id`, `status`, `invited_by`), `seed_tenant_default_roles()` function — **second RBAC system (extended)** |
| 117 | Mar 2026 | Soft-delete columns on 14 tables, `soft_delete_record()` function, `audit_trigger_func()` + triggers on 9 tables |
| **118** | Mar 2026 | `clerk_org_id` migration, `auth_audit_log`, FDW views (`fdw_tenant_users`, `fdw_tenant_roles`, etc.) |
| 126 | Jul 2026 | MDM core tables (`mdm_contacts`, `mdm_cases`) — not IAM |
| 130 | Jul 2026 | Link `customer_contacts.core_contact_id → core_contacts.contact_id` FK |
| 131 | Jul 2026 | Deprecate `tenant_contacts` → renamed to `archived_tenant_contacts` |
| **159** | Jul 2026 | `authority_gates`, `authority_delegations`, `authority_decisions`, `authority_gate_denials`, `fn_evaluate_authority_gate()`, `fn_record_authority_decision()` |
| 160 | Jul 2026 | `system_audit_chain` (hash chaining), `audit_trigger_func_v2()`, audit triggers on 10+ compliance tables |
| **174** | Jul 2026 | `client_portal_access_grants`, `client_portal_invitations`, `communication_threads`, `tenant_branding_config`, `fn_upgrade_portal_access_on_activation()` trigger |
| 175 | Jul 2026 | `tenant_product_entitlements`, `fn_check_entitlement()`, `fn_record_entitlement_usage()` |
| **179** | **Jul 2026** | **ALL 12 CANONICAL IAM TABLES + seed data** |

**Bold entries** = IAM-relevant (create or modify identity/membership/role/permission tables).

---

## APPENDIX: Table Prefix / Naming Conventions

The SaaS Admin database has three naming conventions that evolved over time:

1. **`tenant_*` prefix (003-020):** Early pattern — `tenant_accounts`, `tenant_users`, `tenant_settings`, `tenant_contacts`, `tenant_roles`
2. **`system_*` prefix (003+):** Platform admin scope — `system_admin_users`, `system_audit_log`, `system_staff_users`
3. **`iam_*` prefix (179):** Canonical IAM prefix — `iam_roles`, `iam_permissions`, `iam_access_projection`
4. **No prefix (174-179):** Newer IAM tables — `identity_profiles`, `tenant_memberships`, `platform_staff_memberships`, `authority_grants`, `client_portal_access_grants`

**Binding decision:** `iam_*` prefix is reserved for the canonical role/permission catalogue. Membership tables (`tenant_memberships`, `platform_staff_memberships`) do NOT use the `iam_*` prefix because they bridge between `identity_profiles` and domain entities. The core identity table is `identity_profiles` (no prefix needed — it is THE identity authority).

---

*End of IAM G3 Schema Reconciliation Report*
