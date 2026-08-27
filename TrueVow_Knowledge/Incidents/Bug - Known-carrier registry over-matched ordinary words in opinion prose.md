---
category: bug
title: "Known-carrier registry over-matched ordinary words in opinion prose"
importance: 7
tags: []
file_paths: []
created: 2026-07-09T04:06:36.326586+00:00
updated: 2026-07-09T04:06:36.326586+00:00
memory_id: 4f1a9511-54d8-4cef-8155-1f2739f1169e
---

# Known-carrier registry over-matched ordinary words in opinion prose

extract_carrier's known-carrier list matched homonyms in full opinion text: 'the general rule', 'travelers on the highway', 'nationwide', 'progressive disease', 'Hartford CT'. On 2901 CL records this produced 507 fake 'The General', 234 'The Hartford' etc. Fix: _AMBIGUOUS_CARRIERS set gated by _carrier_in_context (insurance indicator within +-60 chars). Result 1142 clean carriers. Lesson: bounded test on news-highlights did NOT surface this; full-prose opinion text is a different distribution - test enrichment on the ACTUAL corpus type.

---
**Category:** `bug` | **Importance:** 7/10
**Files:** N/A
