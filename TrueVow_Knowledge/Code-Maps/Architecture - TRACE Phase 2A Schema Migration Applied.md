---
category: architecture
title: "TRACE Phase 2A Schema Migration Applied"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T02:55:42.259957+00:00
updated: 2026-07-31T02:55:42.259957+00:00
memory_id: b3e29dbd-8e33-4273-b3cf-a26ec9c7c4de
---

# TRACE Phase 2A Schema Migration Applied

Migration 0017 applied to Supabase Postgres — 31 new tables across 9 layers: global reference (jurisdiction_profiles), tenant-scoped (business_events, policy_records, consent_records), source-linked evidence (source_locations, evidence_facts, fact_versions, contradiction_pairs, missing_evidence_signals), matter structure (incidents, claims, damages), medical (injuries, symptoms, diagnoses, treatment_episodes), workflow (issues, demand_drafts, demand_packages, readiness_assessments, record_completeness_assessments), evidence integrity (chain_of_custody_events, witnesses, witness_statements), insurance/coverage/liability, and client portal (trace_client_access_projections, jurisdiction_activations). Alembic env.py updated with search_path=trace. Ownership model corrected: ClientAccessProjection is TRACE-local temporary mirror of Shared Platform canonical grant. RETAINER never grants MATTER_* scopes.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
