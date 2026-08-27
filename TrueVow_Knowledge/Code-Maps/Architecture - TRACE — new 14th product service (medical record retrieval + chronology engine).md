---
category: architecture
title: "TRACE \u2014 new 14th product service (medical record retrieval + chronology engine)"
importance: 9
tags: []
file_paths: []
created: 2026-07-08T07:46:29.632294+00:00
updated: 2026-07-08T07:46:29.632294+00:00
memory_id: f8a858c8-add4-455a-9103-ec3b2d19ec5b
---

# TRACE — new 14th product service (medical record retrieval + chronology engine)

TRACE (Treatment Record Acquisition and Chronology Engine) is TrueVow's 2nd-stage pipeline product: INTAKE -> TRACE -> SETTLE (Capture -> Build -> Protect). Embedded in the attorney portal, triggered when a lead is marked Retainer Signed. Automates 12-18 hrs/case of medical-record retrieval + source-cited chronology for solo/small PI firms. LOCKED stack (no substitutions): Python3.11/FastAPI, PostgreSQL15 operational + separate pgcrypto AES-256 PHI store, S3 SSE-KMS, AWS Textract OCR, Fax.Plus Enterprise, scispaCy en_core_sci_md, Claude claude-sonnet-4-6 (in-VPC, de-identified) for billing recon, React18+TS, PDF.js, Auth0+MFA, AWS us-east-1/us-west-2, pgaudit+CloudWatch. Hard code-level constraints: prohibited-string filter (raise not replace), Checkpoint-2 fax gate (403 w/o confirmed provider list), demand-ready gate (400 w/ unannotated priority flags), no PHI in URLs/logs/notifications, no client-side PHI. 3 DB roles: trace_app_role, trace_phi_role, trace_readonly_role. Build sequence Part7 gated 1A->1F. Registered in config.yaml as status=building. Confirmation doc produced (TRACE-Phase1A-Confirmation.md) awaiting review before Phase 1A code.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
