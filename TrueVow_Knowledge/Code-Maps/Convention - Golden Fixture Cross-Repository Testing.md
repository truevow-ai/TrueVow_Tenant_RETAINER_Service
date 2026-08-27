---
category: convention
title: "Golden Fixture Cross-Repository Testing"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T02:56:58.058988+00:00
updated: 2026-07-31T02:56:58.058988+00:00
memory_id: 5db6f42b-f665-43f2-b97f-8709174828c7
---

# Golden Fixture Cross-Repository Testing

Created app/shared/contracts.py with frozen contract versions and deterministic golden fixture (make_golden_envelope, make_golden_fixture_json, compute_golden_hmac). Every TrueVow product must deserialize the same 18-field EventEnvelope and compute the same HMAC over the exact raw fixture. Tests at tests/test_golden_fixtures.py validate envelope serialization, roundtrip deserialization, HMAC determinism, evidence manifest completeness (9 refs), and jurisdiction separation (global vs tenant).

---
**Category:** `convention` | **Importance:** 8/10
**Files:** N/A
