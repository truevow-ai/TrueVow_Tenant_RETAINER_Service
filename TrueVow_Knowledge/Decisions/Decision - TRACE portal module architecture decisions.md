---
category: decision
title: "TRACE portal module architecture decisions"
importance: 8
tags: []
file_paths: []
created: 2026-07-24T13:46:30.509826+00:00
updated: 2026-07-24T13:46:30.509826+00:00
memory_id: aedc300c-5df3-4a70-b74c-4201c03a30b2
---

# TRACE portal module architecture decisions

TRACE frontend integrated into Customer Portal (Next.js 14, port 3031, Clerk App3). LEVERAGE hidden from sidebar, replaced by TRACE. Features: 6 pages (landing, cases list, new case wizard, case detail, providers, chronology). Portal-to-backend communication via universal proxy route app/api/trace/[...path]/route.ts that generates HS256 JWT using Node crypto (zero dependencies). Feature gating via billing service with dev fallback. Tenant resolution via useTenantDev() with NEXT_PUBLIC_DEV_TENANT_ID fallback for users without Clerk tenant assignment. DocuSeal and Documo both offline in dev -- case stage advancement forced via DB update for testing.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
