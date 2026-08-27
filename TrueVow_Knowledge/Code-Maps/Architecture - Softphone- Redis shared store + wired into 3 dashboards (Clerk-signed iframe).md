---
category: architecture
title: "Softphone: Redis shared store + wired into 3 dashboards (Clerk-signed iframe)"
importance: 8
tags: []
file_paths: []
created: 2026-07-09T02:20:57.222044+00:00
updated: 2026-07-09T02:20:57.222044+00:00
memory_id: f545f97f-3109-4723-95c9-b344c7f8737f
---

# Softphone: Redis shared store + wired into 3 dashboards (Clerk-signed iframe)

Two wirings completed. (1) REDIS SHARED STORE: new store.py with InMemoryStore + RedisStore behind one interface; get_store() picks Redis when REDIS_URL set, else in-memory, and degrades to in-memory if Redis unreachable at boot (never drops the phone line). registry.py + messages.py now delegate to the store (no more module-level dicts). Redis keys: sp:online (zset by last-seen ts, TTL 90s), sp:assign:<caller> (string), sp:inbox:<identity> (list of JSON, capped 500). Dockerfile CMD now uses WEB_CONCURRENCY env (default 1; raise only with Redis). requirements+redis>=5. Tests: 31 passed + 3 Redis tests self-skip without server (tests/test_store.py). conftest uses store.reset_store() between tests. (2) DASHBOARD INTEGRATION for Sales Ops, Customer Success CORE, SaaS Admin (all App Router + Clerk + npm + @/ alias->root): added to each: lib/softphone/signAgentToken.ts (crypto HMAC mirroring auth.py, base64url agentId.expiry.sig), app/api/softphone/token/route.ts (GET: auth() -> Clerk userId -> signAgentToken -> {token}), components/softphone/Softphone.tsx ('use client' persistent docked iframe bottom-right, useUser, fetches /api/softphone/token, postMessage type:truevow-auth to NEXT_PUBLIC_SOFTPHONE_URL, refreshes token every 45min, toggle button). Mounted <Softphone/> in each (dashboard) layout shell so it survives navigation: Sales layout.tsx (client), SaaS layout.tsx (client), CSM layout-client.tsx. Agent identity = Clerk userId so inbound rings the right agent. Each dashboard env needs NEXT_PUBLIC_SOFTPHONE_URL + SOFTPHONE_SIGNING_SECRET (appended to their env files). signAgentToken.ts type-checks clean. NOTE: the 3 dashboards are separate git repos - their code changes are uncommitted there, not in the CTO repo.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
