---
category: architecture
title: "TRACE Phase 1B COMPLETE + GREEN \u2014 case init + SOL + PHI encryption + provider extraction"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T09:37:20.527336+00:00
updated: 2026-07-08T09:37:20.527336+00:00
memory_id: 00015473-08ab-4ed1-a2e3-cac8e4b9954e
---

# TRACE Phase 1B COMPLETE + GREEN — case init + SOL + PHI encryption + provider extraction

TRACE Phase 1B built and GREEN (25 tests total, ruff+mypy clean; TRACE repo commit a2d2969). Delivered: (1) SOL service app/services/sol.py — full 50-state+DC table (spec 5.4) BUT prefers INTAKE statute snapshot (sol_years/reference) per ADR-000; urgency Standard/Monitor/Urgent/Critical at 180/90/30-day boundaries; mandatory non-dismissible disclaimer on every result; SOL_TABLE_VERSION tracked. (2) PHI store — separate engine (phi_engine/phi_session_maker), Client model on separate PHIBase metadata, AES-256-GCM app-level encryption (app/core/crypto.py, key from KMS/settings not DB); store_client returns opaque client_token; operational DB holds only token. Verified PII encrypted at rest + not in operational DB. (3) POST /api/v1/trace/cases case-init endpoint (spec 4.2): firm-authoritative from Clerk token (body firm_id must match else 403), future-incident-date->400, unknown-state->400, duplicate intake_record_id->409, encrypts PII->PHI, resolves SOL, creates case stage=INITIALIZATION, domain audit case.initialized, triggers provider extraction via BackgroundTasks. (4) NPI Registry client (app/services/npi.py, normalizes CMS JSON, injectable) + provider extraction skeleton (app/services/providers.py) creating UNCONFIRMED providers with HIGH/MEDIUM/LOW confidence; spaCy NER deferred to Phase 1C; Provider model + migration 0002 add extraction_confidence/source_reference. DEFERRED: React portal (frontend, not testable in backend env). Phase 1B acceptance PASSED: case has correct SOL deadline+urgency+disclaimer; PHI encrypted+not in operational DB. NEXT Phase 1C: spaCy en_core_sci_md extraction from intake transcript, provider confirmation checklist CRUD + confirm (Checkpoint 1), HIPAA fax request generation + Fax.Plus transmission.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
