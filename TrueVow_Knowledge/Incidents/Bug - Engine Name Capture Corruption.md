---
category: bug
title: "Engine Name Capture Corruption"
importance: 10
tags: []
file_paths: []
created: 2026-07-30T01:29:22.420987+00:00
updated: 2026-07-30T01:29:22.420987+00:00
memory_id: c0e66599-f799-4ac3-b772-dd1595e20fa4
---

# Engine Name Capture Corruption

From 2026-07-29 test call transcript: contact_name corrupted through 5 different garbage values in a single 13-min call (call me Shaula → Me. Just Yeshua → Normal Conversation. Takes Place → K. P K). Root cause: _try_extract_intro_name and _try_correct_name over-fire on sentence fragments, treating any multi-word input as a name correction. contact_first_name stored as 'call' (from 'you can call me'). Also: workflow resets to greeting node mid-wrap-up after FAQ answer, error node as dead-end trap (6 occurrences), duplicate contact sequences run twice, phone spoken-digit normalization fails for 'nine two one five five five one three three'.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
