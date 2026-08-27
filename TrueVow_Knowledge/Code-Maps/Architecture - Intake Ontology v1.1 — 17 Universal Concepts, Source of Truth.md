---
category: architecture
title: "Intake Ontology v1.1 \u2014 17 Universal Concepts, Source of Truth"
importance: 10
tags: []
file_paths: []
created: 2026-07-30T04:01:46.591009+00:00
updated: 2026-07-30T04:01:46.591009+00:00
memory_id: 7431d1e6-5929-439d-9a7a-1b1ec6c86072
---

# Intake Ontology v1.1 — 17 Universal Concepts, Source of Truth

17 concepts: Person, Caller, Adverse Party, Matter, Event, Location, Timeline, Harm, Medical, Economic Impact, Evidence, Witnesses, Representation, Insurance, Liability, Damages, Disposition. Per-field completion thresholds (0.70-0.95). Provenance priority: spelled 100 > direct_confirmation 90 > direct_answer 85 > extracted 70 > narrative 50 > inferred 30. OntologyResolver: shared singleton, observe() submits observations per field, resolve() picks best using provenance priority, is_complete() checks per-field threshold. 58 node-to-ontology field mappings. Every store_response now submits observation. File: intake_ontology.yaml v1.1

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
