---
category: architecture
title: "TRACE grounded architecture \u2014 platform reality diverges from spec (Clerk not Auth0, Supabase, S3 exists, SigNoz, reuse INTAKE SOL)"
importance: 9
tags: []
file_paths: []
created: 2026-07-08T08:27:12.509673+00:00
updated: 2026-07-08T08:27:12.509673+00:00
memory_id: 421886c7-fe05-4f87-a4ea-bb52f590df6e
---

# TRACE grounded architecture — platform reality diverges from spec (Clerk not Auth0, Supabase, S3 exists, SigNoz, reuse INTAKE SOL)

Codebase exploration of INTAKE/SETTLE/Billing/FM/shared-libraries produced grounded TRACE architecture (see TRACE-Architecture-Decisions.md). KEY FINDINGS: (1) AUTH = Clerk everywhere (3-domain: Platform-Operators/Sales-Support/Tenants), JWKS RS256, MFA via two_factor_enabled. ZERO Auth0. TRACE spec's Auth0 is WRONG -> use Clerk App 3 (Tenants). Needs Privacy-Officer sign-off (deviates from LOCKED). (2) DB = Supabase Postgres + SQLAlchemy2 async + asyncpg + Alembic; RLS via GUC app.current_tenant_id (=Clerk org_id); pooler + statement_cache_size=0. Follow FM pattern. (3) OBJECT STORAGE ALREADY EXISTS: SETTLE app/services/storage/s3_service.py (boto3, presigned, SSE-AES256, us-west-2) — corrects earlier 'no storage' flag. TRACE: S3 via boto3 wrapped in StorageService abstraction, upgraded to SSE-KMS + AWS BAA (PHI). (4) OBSERVABILITY = SigNoz(OTEL)+Sentry, NOT CloudWatch. HIPAA audit = append-only audit_log table (INSERT-only role) + pgaudit. (5) SOL: INTAKE already persists statute snapshot on intake_sessions + 23 jurisdiction JSON files with per-practice-area SOL. REUSE, do not rebuild spec's SOL_TABLE. (6) TRIGGER: INTAKE uses outbox/domain-events (engagement_letter_signed bool + OutboxEvent + CaseCreated). TRACE subscribes to outbox, not sync POST. No cases table exists yet. (7) Tests: pytest+asyncio+SQLite in-memory fallback (conftest) -> enables local Phase 1A acceptance w/o cloud. Alembic migrations. ruff+mypy. (8) Hosting Fly.io (iad)+Docker. ICD/CPT DECISION: per-case client medical bills (PHI) stay in TRACE operational DB (event_nodes + medical_bill_line, RLS firm-segmented); non-PHI CPT/ICD reference catalog -> Billing DB new 'medical_coding' schema (billing tenant_id matches firm; FM legal_entity_id mismatch -> rejected). Do NOT co-mingle client PHI into corporate billing/FM DBs. Extraction via temp spaCy fallback. SIGN-OFF NEEDED: Auth0->Clerk, S3 SSE-KMS+BAA, CloudWatch->SigNoz. STILL OUTSTANDING: updated PRD (still 9 not 12 questions), amended Fly.io+Supabase spec.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
