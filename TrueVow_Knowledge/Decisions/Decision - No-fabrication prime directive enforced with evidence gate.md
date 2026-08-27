---
category: decision
title: "No-fabrication prime directive enforced with evidence gate"
importance: 10
tags: []
file_paths: []
created: 2026-07-10T06:50:54.044325+00:00
updated: 2026-07-10T06:50:54.044325+00:00
memory_id: 58276178-dd72-4b0b-b888-ebc7869d7e06
---

# No-fabrication prime directive enforced with evidence gate

Every field entering settle_verdicts must trace to source_url + appear verbatim in an evidence snippet, else it is stripped; records without verifiable identity are rejected. no_fabrication_gate.verify_record tracks per-field validation_counts + field_evidence (stored in DB columns). Removed all guessing: expert-count split-in-half AND personal_injury_general case_type fallback. Purged 20003 rows, reloaded 11931 verifiable (13725 pass gate; some dedup). Rule: zero records beats fabricated data.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
