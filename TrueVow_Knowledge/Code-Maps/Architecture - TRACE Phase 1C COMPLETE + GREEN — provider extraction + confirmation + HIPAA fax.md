---
category: architecture
title: "TRACE Phase 1C COMPLETE + GREEN \u2014 provider extraction + confirmation + HIPAA fax + delivery webhook"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T10:11:12.023840+00:00
updated: 2026-07-08T10:11:12.023840+00:00
memory_id: 08d35353-c259-4433-83f0-f4ff9a9f62ce
---

# TRACE Phase 1C COMPLETE + GREEN — provider extraction + confirmation + HIPAA fax + delivery webhook

Phase 1C built and GREEN (36 tests total, ruff+mypy clean; TRACE repo commit abd2a29). Delivered: (1) TRANSCRIPT EXTRACTION via app/services/transcript_extractor.py — rule-based patterns for facilities (Hospital/Clinic/Imaging keywords) + Dr. name regex, with guarded spaCy en_core_sci_md for production (requirements-nlp.txt, fallback when not installed). (2) PROVIDER CONFIRMATION CRUD + CHECKPOINT 1 (app/api/v1/routes/providers.py): GET/PUT/POST/DELETE providers, POST /confirm locks the list at case.provider_list_status=CONFIRMED (≥1 CONFIRMED required), RLS firm-scoped, domain audit. Post-confirm editing blocked. Provider stays CONFIRMED (LOCKED is a case-level status, not a provider column — valid_confirmation CHECK friendly). (3) RecordRequest model + migration 0003 (fax_number, fax_transmission_id, status PENDING/SENT/DELIVERED/FAILED, timestamps, RLS). (4) HIPAA COVER SHEET PDF (app/services/cover_sheet.py, reportlab): NO client PII in cover sheet — only opaque case_ref + HIPAA auth reference. Structural no-PII guarantee: the generate() signature accepts only case_ref, provider_name, provider_fax, return_fax, hipaa_auth_ref, record_types. Signed authorization PDF (with PII) is attached separately. (5) Fax.Plus client stub (app/services/fax.py, mockable via FastAPI dependency_overrides). (6) CHECKPOINT 2: POST /requests/send — 403 gate if case.provider_list_status != CONFIRMED; generates cover sheets; transmits via injected fax client; creates RecordRequest rows; marks providers RETRIEVAL; sets case stage to RETRIEVAL; domain audit. GET /requests preview. (7) WEBHOOK: POST /webhooks/fax-status — machine-to-machine (no Clerk session), optional shared-secret auth; updates RecordRequest status+confirmed_at; SYSTEM audit. (8) E2E test confirms full flow: case init → provider extraction → confirm Checkpoint1 → preview → send Checkpoint2 → webhook delivery → DB DELIVERED. Checkpoint-2 gate tested: send blocked before confirm = 403. Phase 1C ACCEPTANCE PASSED: all steps audited, cover sheet PII-free, true integration test. NEXT Phase 1D: fax-receive webhook + manual upload → Textract OCR → document classification+indexing → clinical event extraction (spaCy)→ chronology_entries with source citations → gap detection → billing recon with prohibited-string filter. Biggest remaining Phase 1 build phases.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
