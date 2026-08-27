# IAM Current State Inventory — IAM-G0

**Date:** 2026-08-02
**Gate:** IAM-G0 — Read-Only Inventory
**Status:** COMPLETE

---

## Executive Summary

Clerk is the sole human identity provider across 6 frontend services and 3 Python backend services. Supabase is used exclusively as a data layer, not for human authentication. No `auth.users`, `profiles`, or `memberships` tables exist in any migration. RBAC is partially implemented in SaaS Admin (`tenant_roles`, `tenant_users`, `tenant_user_roles`) and INTAKE (`user_roles`). Clerk organization IDs are extracted from JWT claims but not persisted in the database. Zero Clerk webhook routes or webhook secrets are configured. The `@truevow/auth-client` shared library wraps Clerk and enforces the 3-domain architecture.

---

## Service Inventory

### Clerk Frontend SDK (6 services)

| Service | Clerk App | Clerk packages | Auth pattern |
|---|---|---|---|
| SaaS Admin | App 1 (Platform Operators) | `@clerk/nextjs` | `clerkMiddleware`, `auth()`, `useUser`, `<SignIn>`, `<ClerkProvider>` |
| Sales Ops | App 2 (Sales & Support) | `@clerk/nextjs` | `clerkMiddleware`, `auth()`, `useUser`, `<SignIn>`, `<ClerkProvider>` |
| CS Support Core | App 1 (Platform Operators) | `@clerk/nextjs` | `clerkMiddleware`, `auth()`, `useUser`, `<SignIn>`, `UserButton` |
| First-Line Support | App 2 (Sales & Support) | `@clerk/nextjs` | `clerkMiddleware`, `auth()`, `useUser`, `<SignIn>`, `<SignUp>` |
| Customer Portal | App 3 (Tenants) | `@clerk/nextjs` | **Heaviest usage**: `clerkClient()`, `auth()`, `useAuth`, `useUser`, `useClerk`, `<SignIn>`, `<SignUp>`, `<SignOutButton>`, `UserButton` |
| Billing Service | App 3 (Tenants) | `@clerk/nextjs` | `clerkMiddleware`, `useUser`, `<SignedIn>`, `<SignedOut>`, `<SignInButton>`, `<UserButton>` |

### Clerk JWT Verification Only (3 services)

| Service | Pattern | Details |
|---|---|---|
| INTAKE (Python) | `clerk_sdk` JWT verification | `verify_clerk_token()`, `clerk_middleware()`, reads `CLERK_SECRET_KEY` |
| RETAINER (Python) | JWKS RS256 | `CLERK_JWKS_URL`, `CLERK_ISSUER`, `CLERK_AUDIENCE` |
| TRACE (Python) | JWKS RS256 (cached) | `PyJWKClient` with `_JWKSCache`, `AUTH_MODE=clerk` |

### No Clerk Dependencies (9 services)

SETTLE, VERIFY, COMMAND, LEVERAGE, Platform Analytics, Communications, Internal Ops, Financial Management, 2026 Website.

### Shared Library

`@truevow/auth-client` (`shared-libraries/auth-client/`) wraps `@clerk/backend` and `@clerk/nextjs`. Provides `ClerkWrapper`, `TokenManager`, `CrossDomainExchange`. Enforces 3-domain architecture. Extracts `orgId` from JWT claims.

---

## Clerk Configuration

### Three Clerk Apps

| App | Instance ID | Services |
|---|---|---|
| App 1 — Platform Operators | `app_39dFtR56NG6WsR4fndruMyKYuJc` | SaaS Admin, CS Support Core |
| App 2 — Sales & Support | `ins_39dIJAreQQeJdIW12QDHAv8RX6Y` | Sales Ops, First-Line Support |
| App 3 — Tenants | `app_39dIvhD9icLQF5Ydy95eFC5X8t2` | Customer Portal, Billing |
