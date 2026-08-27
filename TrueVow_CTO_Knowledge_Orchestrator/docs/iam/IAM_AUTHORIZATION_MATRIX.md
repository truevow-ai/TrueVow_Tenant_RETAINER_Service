# IAM Authorization Matrix — IAM-G1

**Frozen:** 2026-08-02

---

## Role → Permission Mapping

| Role | members.* | intake.* | matters.* | documents.* | billing.* | recordings.* | transcripts.* | tenant.settings.* | platform.* | client.* |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TENANT_OWNER | invite/read/manage | read/update | read/update | upload | read/manage | listen | read | read/manage | — | — |
| TENANT_ADMIN | invite/read/manage | read/update | read | upload | read | listen | read | read/manage | — | — |
| ATTORNEY | read | read/update | read/update | upload | — | listen | read | read | — | — |
| INTAKE_MANAGER | read | read/update | read | — | — | listen | read | read | — | — |
| CASE_STAFF | read | read | read/update | upload | — | — | read | — | — | — |
| BILLING_MANAGER | read | — | read | — | read/manage | — | — | read | — | — |
| VIEWER | — | read | read | — | — | — | — | — | — | — |
| PLATFORM_OWNER | — | — | — | — | — | — | — | — | ALL | — |
| PLATFORM_ADMIN | — | — | — | — | — | — | — | — | tenants.read/create/suspend, entitlements.*, staff.*, audit.read | — |
| CSM | — | — | — | — | — | — | — | — | tenants.read, entitlements.read, staff.read | — |
| SUPPORT_AGENT | — | — | — | — | — | — | — | — | tenants.read | — |
| SALES_OPS_ADMIN | — | — | — | — | — | — | — | — | — | — |
| CLIENT_PORTAL_USER | — | — | — | — | — | — | — | — | — | matter.read, documents.read, messages.send |

## Application Access Matrix

| Application | TENANT_OWNER | ATTORNEY | CSM | PLATFORM_ADMIN | SALES_OPS_ADMIN | CLIENT |
|---|---|---|---|---|---|---|---|
| SaaS Admin | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ |
| Sales Ops | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| Customer Portal | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| INTAKE | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| TRACE | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| SETTLE | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |

## Membership Access Rules

1. No membership = no access. Authenticated user without membership is denied.
2. Suspended identity = denied everywhere.
3. Revoked membership = denied for that tenant/application.
4. Tenant A cannot read Tenant B. Cross-tenant access blocked by RLS.
5. Platform staff do not bypass tenant isolation by default. Tenant access requires explicit, auditable, time-bound impersonation.
6. Client users restricted to authorized matters only.
7. Machine routes (HMAC) never require human sessions.
8. Service-role credentials never exposed in browser.

## Authority Class Gates

| Operation | Required Authority |
|---|---|
| Tenant activation | FIRM_POLICY + PLATFORM_ADMIN |
| Representation decision | ATTY_AUTH |
| Client settlement acceptance | CLIENT_AUTH |
| Policy acceptance | FIRM_POLICY |
| Administrative override | SYS_ADMIN (audited) |
| Prohibited operations | PROHIBITED (platform-enforced block) |
