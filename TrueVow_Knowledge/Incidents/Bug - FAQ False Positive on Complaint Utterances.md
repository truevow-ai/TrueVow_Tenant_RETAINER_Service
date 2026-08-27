---
category: bug
title: "FAQ False Positive on Complaint Utterances"
importance: 8
tags: []
file_paths: []
created: 2026-07-31T05:45:54.356183+00:00
updated: 2026-07-31T05:45:54.356183+00:00
memory_id: 252e5513-0395-488a-8c15-fbccae8e67fe
---

# FAQ False Positive on Complaint Utterances

From 2026-07-31 call: caller said 'you're having trouble processing it because you're not getting a consultation from the LLM' — FAQ matched on 'consultation' keyword, answered with fee policy. Caller was complaining about AI, not asking about pricing. Fix: added _classify_utterance gate before FAQ matching — complaint/refusal utterances skip FAQ injection. Also added 'having trouble' and 'not get' to complaint regex patterns.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
