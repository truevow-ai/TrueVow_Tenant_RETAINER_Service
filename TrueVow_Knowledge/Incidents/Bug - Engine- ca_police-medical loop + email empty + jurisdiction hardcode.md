---
category: bug
title: "Engine: ca_police/medical loop + email empty + jurisdiction hardcode"
importance: 10
tags: []
file_paths: []
created: 2026-08-01T03:49:21.510692+00:00
updated: 2026-08-01T03:49:21.510692+00:00
memory_id: eee7d4ee-7505-4bfc-92c2-0e4109e978b0
---

# Engine: ca_police/medical loop + email empty + jurisdiction hardcode

Three critical bugs from Aug 1 call: (1) ca_police and ca_medical_treatment nodes cycle infinitely on 'no' answers — the ca workflow ladder has a next-pointer loop. (2) Email verify prompt shows empty '{contact_email}' — email extraction stores raw text instead of parsed email address. (3) conflict_check_prior_rep routes 'no' to ca_jurisdiction regardless of practice area — should route to identify_practice_area when practice area unknown. Also: Gemini STOP errors after long calls suggesting context overflow.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
