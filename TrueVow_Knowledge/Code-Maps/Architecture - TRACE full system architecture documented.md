---
category: architecture
title: "TRACE full system architecture documented"
importance: 10
tags: []
file_paths: []
created: 2026-07-24T13:46:14.498941+00:00
updated: 2026-07-24T13:46:14.498941+00:00
memory_id: 42e640f6-a5ea-40d5-83a3-3813a0193463
---

# TRACE full system architecture documented

TRACE service (port 3036) runs as second pipeline stage (INTAKE -> TRACE -> SETTLE). Backend: Python FastAPI with JWT auth, Supabase Postgres+Storage, DeepSeek LLM. Portal: Next.js 14 at port 3031 with 6 TRACE pages, universal proxy route generating HS256 JWT. 28 API endpoints covering cases, providers, fax, documents, chronology, liens, export, webhooks. Inbound email via Resend webhook, inbound fax via Documo callback. 60/60 tests passing. Documentation at docs/00-Planning/TRACE-Agent-Coding-Instructions.md Appendix A.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
