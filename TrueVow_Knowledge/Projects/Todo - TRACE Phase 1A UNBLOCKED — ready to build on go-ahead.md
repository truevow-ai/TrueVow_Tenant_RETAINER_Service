---
category: todo
title: "TRACE Phase 1A UNBLOCKED \u2014 ready to build on go-ahead"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T08:38:10.110494+00:00
updated: 2026-07-08T08:38:10.110494+00:00
memory_id: 17e2e8ba-87b3-4d49-acb7-c0b2f60b9a7d
---

# TRACE Phase 1A UNBLOCKED — ready to build on go-ahead

Owner confirmed PRD §12 is genuinely 9 open questions; the perceived 'three extra' were architectural items now RESOLVED: (1) cloud provider = Fly.io+Supabase; (2) LLM BAA = Azure OpenAI GPT-4o-mini / DeepSeek prohibited; (3) billing repo = CPT/ICD catalog + PHI both in TRACE's own DB, temp spaCy fallback, billing/FM untouched. All 3 spec deviations approved (Clerk not Auth0; S3 SSE-KMS+BAA; SigNoz+pgaudit not CloudWatch). No remaining blockers. TRACE-Phase1A-Confirmation.md refreshed to v2 (platform-grounded). Phase 1A deliverables: repo scaffold + FastAPI skeleton (Clerk JWKS + audit middleware) + Alembic schema/roles/RLS (operational + separate PHI store) + StorageService(S3) stub + Dockerfile + fly.toml + pytest/SQLite-fallback harness. Acceptance gate to 1B: authed call logged in audit_log; unauth->401; firm-A cannot read firm-B. AWAITING explicit go-ahead to write Phase 1A code.

---
**Category:** `todo` | **Importance:** 8/10
**Files:** N/A
