# Identity Data Model — IAM-G1

**Frozen:** 2026-08-02
**Version:** 1.0.0

---

## Entity Relationship

```
auth.users (Supabase Auth)
    ↓ 1:1
identity_profiles (SaaS Admin)
    ↓ 1:N
tenant_memberships ──────→ tenant_accounts
platform_staff_memberships
client_portal_memberships ─→ matters
    ↓
membership_role_assignments ─→ roles
    ↓
role_permissions ─→ permissions
```

## Tables

### identity_profiles

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| auth_user_id | UUID | FK → auth.users.id |
| display_name | TEXT | |
| primary_email | TEXT | |
| phone | TEXT | |
| profile_status | TEXT | ACTIVE, SUSPENDED, DEACTIVATED |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |
| suspended_at | TIMESTAMPTZ | |
| deactivated_at | TIMESTAMPTZ | |

No password hashes or refresh tokens. Supabase Auth owns secrets.

### tenant_memberships

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| identity_profile_id | UUID FK | → identity_profiles |
| tenant_id | UUID FK | → tenant_accounts |
| membership_status | TEXT | INVITED, ACTIVE, SUSPENDED, REVOKED |
| joined_at | TIMESTAMPTZ | |
| suspended_at | TIMESTAMPTZ | |
| revoked_at | TIMESTAMPTZ | |
| created_by | UUID | |
| authority_reference | UUID | Audit trail |

UNIQUE (identity_profile_id, tenant_id)

### platform_staff_memberships

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| identity_profile_id | UUID FK | → identity_profiles |
| application_code | TEXT | saas-admin, sales-ops, csm-core, billing |
| membership_status | TEXT | INVITED, ACTIVE, SUSPENDED, REVOKED |
| granted_by | UUID | |
| granted_at | TIMESTAMPTZ | |
| expires_at | TIMESTAMPTZ | NULL = permanent |
| revoked_at | TIMESTAMPTZ | |

### client_portal_memberships

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| identity_profile_id | UUID FK | → identity_profiles |
| tenant_id | UUID FK | → tenant_accounts |
| matter_id | UUID FK | → matters. NULL = firm-wide |
| allowed_portal | TEXT | customer-portal, client-portal |
| membership_status | TEXT | INVITED, ACTIVE, SUSPENDED, REVOKED |

### roles

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| code | TEXT UNIQUE | TENANT_OWNER, ATTORNEY, etc. |
| name | TEXT | Human-readable |
| domain | TEXT | tenant, platform, client |

### permissions

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| code | TEXT UNIQUE | members.invite, intake.read, etc. |
| name | TEXT | |
| domain | TEXT | tenant, platform |

### role_permissions

| Column | Type | Notes |
|---|---|---|
| role_id | UUID FK | → roles |
| permission_id | UUID FK | → permissions |

### membership_role_assignments

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| membership_table | TEXT | tenant_memberships, platform_staff_memberships, client_portal_memberships |
| membership_id | UUID | Polymorphic FK |
| role_id | UUID FK | → roles |
| assigned_by | UUID | |
| assigned_at | TIMESTAMPTZ | |
| revoked_at | TIMESTAMPTZ | |

### application_access_grants

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| identity_profile_id | UUID FK | → identity_profiles |
| application_code | TEXT | |
| granted_by | UUID | |
| granted_at | TIMESTAMPTZ | |
| revoked_at | TIMESTAMPTZ | |

### authority_grants

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| identity_profile_id | UUID FK | → identity_profiles |
| authority_class | TEXT | SYS_ADMIN, FIRM_POLICY, STAFF_AUTH, ATTY_AUTH, CLIENT_AUTH, PROHIBITED |
| scope_tenant_id | UUID | NULL = platform-wide |
| granted_by | UUID | |
| granted_at | TIMESTAMPTZ | |
| revoked_at | TIMESTAMPTZ | |

### identity_audit_events

| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| identity_profile_id | UUID FK | → identity_profiles |
| event_type | TEXT | IdentityProfileCreated, MembershipGranted, etc. |
| event_payload | JSONB | |
| actor_id | UUID | |
| occurred_at | TIMESTAMPTZ | |

### iam_access_projection (per-product local copy)

| Column | Type | Notes |
|---|---|---|
| identity_id | UUID | |
| application_code | TEXT | |
| tenant_id | UUID | NULL for platform staff |
| membership_status | TEXT | |
| role_codes | TEXT[] | |
| permission_codes | TEXT[] | |
| authorization_version | INTEGER | |
| updated_at | TIMESTAMPTZ | |

## Invitation Lifecycle

```
PENDING → ACCEPTED
PENDING → EXPIRED
PENDING → REVOKED
ACCEPTED → (membership becomes ACTIVE)
```

Supabase Auth sends invitation email. SaaS Admin tracks invitation state in `tenant_memberships` / `platform_staff_memberships`.
