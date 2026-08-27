---
category: decision
title: "vNext Defect Fix Prescriptions"
importance: 9
tags: []
file_paths: []
created: 2026-08-12T15:45:44.226085+00:00
updated: 2026-08-12T15:45:44.226085+00:00
memory_id: d832faf9-144a-4251-8a26-9ad62f37847d
---

# vNext Defect Fix Prescriptions

3 core defects with specific fixes: D1 rear-ended — normalize punctuation/hyphens before classification (not spelling variants). D2 hired-a-lawyer — alias lawyer/attorney for retained/hired phrases. D3 ambiguity — semantic rules: explicit 'didn't retain/did not hire/consultation only' → consulted_only; indirect 'never signed' → clarify. Not just confidence threshold. 2 test defects: scanner exclusions (comments, own test file).

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
