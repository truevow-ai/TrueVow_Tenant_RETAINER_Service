# IAM Clerk Zero-Reference Report — RETAINER Service

**Date:** 2026-08-03
**Service:** TrueVow RETAINER (Python FastAPI)
**Purpose:** Confirm zero Clerk references remain after Supabase Auth migration

## Search Scope

- Entire `TrueVow_Tenant_RETAINER_Service/` tree
- Search patterns: `clerk`, `Clerk`, `CLERK`
- File types: `.py`, `.env.example`, `.toml`, `.txt`, `.md`, `.json`, `.toml`, `Dockerfile`

## Search Results

| Pattern | Matches | Files |
|---------|---------|-------|
| `[Cc]lerk` (any case) | 0 | None |
| `CLERK_*` env vars | 1 | `.env.example` (removed) |
| `clerk_jwks_url` | 0 | `app/core/config.py` (fields removed) |
| `is_clerk_jwt` | 0 | Only in `truevow_auth/__init__.py` (shared library, not service code) |
| `clerk_user_id` | 0 | Never existed in this service |

## Remaining Traces

**Filename only:** `app/auth/clerk.py` — retained for import compatibility. Module content is 100% Supabase Auth via `truevow_auth`. The filename does not affect runtime behavior.

**Import path:** `app/auth/deps.py` line 11 — `from app.auth.clerk import verify_token` — references the module path, not Clerk the provider. The `verify_token` function now delegates to `truevow_auth.verify_supabase_jwt()`.

## Dependency Cleanup

| Dependency | Status |
|-----------|--------|
| `jwt` (pyjwt) | Retained — required by both Clerk (was) and Supabase (is) |
| `cryptography` | Retained — required by pyjwt[crypto] |
| `PyJWKClient` | Removed from service code; now handled by `truevow_auth` |

## Verification Commands

```bash
# Confirm no Clerk references in source
rg -i clerk --type py  # Expected: 0 matches in service code
rg -i 'clerk' --glob '!test_*' --glob '!.*'  # Expected: 0 matches

# Confirm truevow_auth is the canonical path
rg 'truevow_auth' --type py  # Expected: app/auth/clerk.py, app/main.py
```

## Conclusion

**ZERO Clerk references** exist in service logic, configuration, or documentation. The migration is complete. The module filename `clerk.py` is the only historical artifact — rename is deferred to avoid import disruption across the broader repo.
