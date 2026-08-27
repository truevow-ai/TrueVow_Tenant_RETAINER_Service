---
category: decision
title: "TRACE build decisions \u2014 storage pending Fly.io+Supabase spec amendment; billing recon uses temp fallback"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T08:08:51.156446+00:00
updated: 2026-07-08T08:08:51.156446+00:00
memory_id: 599e90b8-322a-4331-849f-007b25ff0158
---

# TRACE build decisions — storage pending Fly.io+Supabase spec amendment; billing recon uses temp fallback

Resolved with product owner after reviewing revised TRACE-Technical-Implementation-Spec.md (1119 lines, 2026-07-08 11:02): (1) FLAG 1 STORAGE/AUDIT: The spec's [IMPLEMENTATION CHOICE] 'match your existing cloud' tables list only AWS/GCP/Azure, but verified TrueVow hosting is Fly.io + Docker + Supabase Postgres (fly.toml in Billing/SETTLE/TenantApp; aws-1-us-east-1.pooler.supabase.com; supabase>=2.0.0). No existing HIPAA-BAA object storage found. OWNER DECISION: owner will AMEND the spec's IMPLEMENTATION CHOICE tables to include Fly.io+Supabase before Phase 1A storage/audit is built. Phase 1A ON HOLD until amended spec lands. (2) FLAG 2 BILLING RECON: Verified FM/billing repos are corporate/SaaS finance (AR/AP/GL/treasury/payroll/intercompany + billing sync/webhook), NOT medical CPT/ICD-10. §5.6 premise 'billing repo owns CPT/ICD-10' is false for this codebase. OWNER DECISION: use the temporary spaCy CPT/ICD fallback from faxed BILLING docs, marked TODO, when §5.6 is eventually built (Phase 1D/4). (3) LOCKED: billing LLM = Azure OpenAI GPT-4o-mini; DeepSeek PROHIBITED any version (no BAA, China residency). (4) STILL BLOCKED: PRD §12 still lists 9 open questions, owner says 12 — awaiting updated PRD. Governance in force: locked-by-default, discretion only within [IMPLEMENTATION CHOICE], flag-and-wait, no unilateral resolution of §12.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
