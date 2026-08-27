# Clerk Dependency Register — IAM-G0

**Status:** COMPLETE
**Removal target:** IAM-G5

---

## Direct `@clerk/*` Package Dependencies

| Service | Package | Version |
|---|---|---|
| SaaS Admin | `@clerk/nextjs` | `^6.36.2` |
| Sales Ops | `@clerk/nextjs` | `^6.36.2` |
| CS Support Core | `@clerk/nextjs` | `^6.36.2` |
| First-Line Support | `@clerk/nextjs` | `^6.36.2` |
| Customer Portal | `@clerk/nextjs` | `^6.36.2` |
| Billing Service | `@clerk/nextjs` | `^6.36.2` |
| `@truevow/auth-client` | `@clerk/nextjs`, `@clerk/backend` | `^6.36.2`, `^1.0.0` |

## Clerk Middleware (9 files)

| Service | File | Lines |
|---|---|---|
| SaaS Admin | `middleware.ts` | 1-73 |
| Sales Ops | `middleware.ts` | 12-67 |
| CS Support Core | `middleware.ts` | 1, 17 |
| First-Line Support | `middleware.ts` | 1, 111 |
| Customer Portal | `middleware.ts` | 1-66 |
| Customer Portal | `middleware-AmmarZayn.ts` | 4 |
| Billing Service | `ui/middleware.ts` | 1-12 |
| INTAKE (Python) | `app/middleware/clerk_auth.py` | 191 |
| `@truevow/auth-client` | `src/clerk-wrapper.ts` | 175 |

## Clerk Server Functions — `auth()` callers (100+ sites)

Most heavily used in: SaaS Admin (10+ routes), Sales Ops (50+ routes), Customer Portal (core dependency), CS Support Core (30+ routes), First-Line Support (15+ routes).

## Clerk UI Components

| Component | Services |
|---|---|
| `<ClerkProvider>` | SaaS Admin, Sales Ops, CS Support Core, First-Line Support, Customer Portal, Billing |
| `<SignIn />` | SaaS Admin, Sales Ops, CS Support Core, First-Line Support, Customer Portal, Billing |
| `<SignUp />` | SaaS Admin, First-Line Support, Customer Portal, Billing |
| `<UserButton>` | Sales Ops, CS Support Core, First-Line Support, Customer Portal, Billing |
| `<SignedIn>`, `<SignedOut>`, `<SignInButton>` | Billing |
| `<SignOutButton>` | Customer Portal |
| `useUser` | All 6 frontend services |
| `useAuth` | Customer Portal, Billing |
| `useClerk` | Customer Portal |

## Clerk Programmatic API

Only Customer Portal uses `clerkClient()` (for `provision-first-admin`, `team/invite`, user management).

## Clerk Environment Variables (12 env files affected)

Found in: `.env.local.backup.txt` (Cursor root), CTO Orchestrator `.env.local`, Communications `.env.local`, TRACE `.env.local`, RETAINER `.env.local`, INTAKE `.env.local`.

## Clerk Webhooks

**Zero** configured. `CLERK_WEBHOOK_SECRET` not found in any file.

## Clerk Organization IDs

Extracted from JWT claims in `clerk-wrapper.ts:83` but NOT persisted in any database table.
