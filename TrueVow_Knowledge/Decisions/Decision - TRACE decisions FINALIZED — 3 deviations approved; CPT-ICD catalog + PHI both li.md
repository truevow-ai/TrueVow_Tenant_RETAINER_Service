---
category: decision
title: "TRACE decisions FINALIZED \u2014 3 deviations approved; CPT/ICD catalog + PHI both live in TRACE's own DB"
importance: 9
tags: []
file_paths: []
created: 2026-07-08T08:33:47.530982+00:00
updated: 2026-07-08T08:33:47.530982+00:00
memory_id: aa8e15d0-45c9-4ca2-8dfb-3603ee450ba1
---

# TRACE decisions FINALIZED — 3 deviations approved; CPT/ICD catalog + PHI both live in TRACE's own DB

Product owner (2026-07-08) APPROVED all 3 grounded deviations from spec LOCKED Section 2: (1) Auth = Clerk (App 3 Tenants), NOT Auth0; (2) Object storage = S3 via boto3 (following SETTLE s3_service.py) upgraded to SSE-KMS + AWS BAA for PHI bucket; (3) Observability = SigNoz(OTEL)+Sentry + append-only audit_log table + pgaudit, NOT CloudWatch. ICD/CPT PLACEMENT FINAL: owner correctly noted billing DB = single source of truth for SaaS subscriptions+metering only, and TRACE is the heavy consumer of the code catalog. DECISION: BOTH the per-case PHI medical bill lines AND the non-PHI CPT/ICD reference catalog live in TRACE's OWN operational DB (medical_bill_line + event_nodes for PHI, firm-RLS; cpt_reference + icd10_reference versioned catalog tables). Billing and FM schemas UNTOUCHED. Rationale: consumer co-location avoids cross-service latency on billing-recon hot path; keeps billing pure (subscriptions) and FM pure (corporate finance); TRACE owns catalog versioning lifecycle. Extraction via temp spaCy fallback from faxed BILLING docs (TODO), no rebuild. STILL BLOCKING Phase 1A code: (a) updated PRD still shows 9 open questions not 12; (b) amended Fly.io+Supabase spec not yet issued. Full detail in TRACE-Architecture-Decisions.md.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
