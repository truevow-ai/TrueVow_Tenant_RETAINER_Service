---
category: decision
title: "No-fabrication is now permanent process (RULE 0) across all pipelines"
importance: 9
tags: []
file_paths: []
created: 2026-07-10T15:48:30.610118+00:00
updated: 2026-07-10T15:48:30.610118+00:00
memory_id: 641c26bb-7bd2-4b27-9da9-bba23fa3963c
---

# No-fabrication is now permanent process (RULE 0) across all pipelines

Codified into AGENTS.md as RULE 0 non-negotiable. Two-gate pipeline (no_fabrication_gate + verdict_validator) for verdicts; cis_fabrication_gate for carriers; govdata verify_and_write_jsonl for govdata. All require source_url+verbatim evidence+integrity. recover_rejects.py re-verifies rejects against sources but only recovers missing-EVIDENCE cases, never missing-VALUE (classification) cases - measured 0/112556 recoverable in current set, correctly (criminal cases mis-flagged by injury keywords). Rejected/quarantined records all preserved on disk for future re-verification.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
