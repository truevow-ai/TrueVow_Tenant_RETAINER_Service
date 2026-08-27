# IAM-G1 — Canonical Contract Freeze — COMPLETE

**Date:** 2026-08-02
**Status:** FROZEN

---

## Artifacts Produced

| # | Artifact | Contents |
|---|---|---|
| 1 | `IAM_TARGET_ARCHITECTURE.md` | Authority boundaries, trust domains, JWT validation patterns, cross-service authorization projections |
| 2 | `IDENTITY_DATA_MODEL.md` | 12 tables: identity_profiles, tenant_memberships, platform_staff_memberships, client_portal_memberships, roles, permissions, role_permissions, membership_role_assignments, application_access_grants, authority_grants, identity_audit_events, iam_access_projection |
| 3 | `ROLE_PERMISSION_CATALOGUE.yaml` | 17 roles (7 tenant, 9 platform, 1 client), 27 permissions (15 tenant, 9 platform, 3 client), 6 authority classes with role mapping |
| 4 | `APPLICATION_CATALOGUE.yaml` | 12 applications with domain, port, owner, auth requirements |
| 5 | `IAM_EVENT_CATALOGUE.yaml` | 45 events across identity, membership, roles, application access, authority, invitation, RLS categories |
| 6 | `IAM_AUTHORIZATION_MATRIX.md` | Role→permission matrix, application access matrix, membership access rules, authority class gates |

## IAM-G2 Implementation (in progress)

| File | Purpose |
|---|---|
| `supabase/migrations/179_iam_identity_core_foundation.sql` | Creates 12 IAM tables with RLS, seeds 17 roles + 27 permissions |
| `lib/auth/supabase-jwt.ts` | Server-side JWT verification via JWKS, identity resolution |
| `lib/auth/supabase-middleware.ts` | Drop-in replacement for clerkMiddleware, public route support, machine route bypass |
| `lib/auth/supabase-provider.tsx` | Client-side Supabase Auth provider replacing ClerkProvider |
