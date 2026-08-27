---
category: architecture
title: "Unified Contact Candidate Ingress"
importance: 10
tags: []
file_paths: []
created: 2026-08-06T17:28:46.487979+00:00
updated: 2026-08-06T17:28:46.487979+00:00
memory_id: 5150abdb-b38b-4110-9914-647af9f9dca1
---

# Unified Contact Candidate Ingress

Implemented generic TaskCandidateIngress processor for all three contact actions (CAPTURE_NAME/EMAIL/PHONE_RESULT). Keyed HMAC-SHA256 fingerprinting, tenant-scoped receipt repository with durable replay/conflict handling, FSM-owned state_version mutation (processor reads from FSM after transition, never calculates independently). 148 tests pass. Commit 891eec8 on review/tv-intake-engine-p1-02e-r1.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
