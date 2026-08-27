---
category: bug
title: "INTAKE engine: hint classification is firing correctly \u2014 complaint detected"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T05:25:57.255163+00:00
updated: 2026-07-31T05:25:57.255163+00:00
memory_id: 1e895361-18af-4338-bd65-0597b7019978
---

# INTAKE engine: hint classification is firing correctly — complaint detected

Bridge classification matches r'why (?:are you|did you|would you|do you)' → complaint. Hint IS being sent to the engine. The gap is that text_input node path at workflow_engine.py:951 is not gated by the hint flag — _extract_name_from_phrase runs on complaint text, storing it as name. Fix is one engine gate: check hint before name extraction in text_input nodes. Owner: ghaus-fsd.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
