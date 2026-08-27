---
category: bug
title: "INTAKE engine: call autopsy \u2014 5 failures from bridge testing"
importance: 9
tags: []
file_paths: []
created: 2026-07-31T05:25:54.321730+00:00
updated: 2026-07-31T05:25:54.321730+00:00
memory_id: df7e71c6-9dcc-4b33-b89e-ef4a64e1fd8d
---

# INTAKE engine: call autopsy — 5 failures from bridge testing

1) Speak to attorney skips entire intake (routing design). 2) intake_summary fires with only name+phone. 3) Complaint text stored as name — hint gate missing at workflow_engine.py:951 text_input path. 4) Duplicate contact capture after summary complaint. 5) Garbage name → verify loop → caller hangs up. Root cause for #3: lines 748-756 gate only _try_extract_intro_name and _try_correct_name, but _extract_name_from_phrase at line 978 runs regardless. Fix: add hint check at line 951 before name extraction in text_input nodes. Owner: ghaus-fsd.

---
**Category:** `bug` | **Importance:** 9/10
**Files:** N/A
