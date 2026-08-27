---
category: decision
title: "Multi-source corroboration as machine verification"
importance: 9
tags: []
file_paths: []
created: 2026-07-11T07:50:01.676530+00:00
updated: 2026-07-11T07:50:01.676530+00:00
memory_id: cfccf09f-6c9e-40db-9fe0-a233b42f4c94
---

# Multi-source corroboration as machine verification

corroborate_verdicts.py: promote settle_verdicts pending->verified only when same case in >=2 independent sources (host-distinguished: static.case.law/CAP, courtlistener, morelaw) agree on amount within 1pct. Match key: shared reporter citation (from source_notes.official_citation) strongest, else normalized case_name+state+amount. 1249/12444 corroborated in dry-run. Disagreement (RJ Reynolds 20M vs 21M) / single-source / same-host-twice never promote. Records corroborating_sources evidence. Migration c0d1e2f3a4b5 + live promotion pending Supabase pooler recovery. This is the machine substitute for the not-yet-available human verifier; law-firm verification later layers ON TOP as a gold tier.

---
**Category:** `decision` | **Importance:** 9/10
**Files:** N/A
