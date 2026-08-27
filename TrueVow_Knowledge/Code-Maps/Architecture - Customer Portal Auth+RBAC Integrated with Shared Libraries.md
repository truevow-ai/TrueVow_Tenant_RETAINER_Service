---
category: architecture
title: "Customer Portal Auth+RBAC Integrated with Shared Libraries"
importance: 9
tags: []
file_paths: []
created: 2026-07-01T01:20:53.829338+00:00
updated: 2026-07-01T01:20:53.829338+00:00
memory_id: 4b1c5c7e-6ebc-4d66-b78c-a30c5771531f
---

# Customer Portal Auth+RBAC Integrated with Shared Libraries

Customer Portal now delegates to @truevow/rbac-engine and @truevow/auth-client via rewritten lib/auth/guard.ts. Backward-compatible API surface preserved (withAuth, withPermission, withLevel, withTenantScope). Shared libraries added as file: dependencies in package.json. Local RoleLevel/Permission/ROLE_REGISTRY enums replaced with imports from shared rbac-engine. Domain enforcement, cross-domain support, and impersonation tracking now available.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
