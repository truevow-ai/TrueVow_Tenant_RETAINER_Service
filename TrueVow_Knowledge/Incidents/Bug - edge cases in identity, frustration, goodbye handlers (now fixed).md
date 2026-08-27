---
category: bug
title: "edge cases in identity, frustration, goodbye handlers (now fixed)"
importance: 7
tags: []
file_paths: []
created: 2026-07-14T18:56:14.168278+00:00
updated: 2026-07-14T18:56:14.168278+00:00
memory_id: d0c10a4c-caf4-435a-b8af-d042ae5453df
---

# edge cases in identity, frustration, goodbye handlers (now fixed)

Comprehensive edge case testing revealed coverage gaps: identity handler missed 'is anyone actually there' and 'who am I talking to', frustration had a FALSE POSITIVE on 'the same thing happened to my sister' and missed 8 phrasings ('taking forever','wasting my time','I have had enough','just stop' etc.), goodbye missed 5 patterns ('forget it','I need to go','talk to you later','Im hanging up','that is it Im out'), name extraction failed on 'Its just Yasha' (multi-strip loop), 'My name? Its Yasha' (mid-sentence question marks from STT), and names with apostrophes/hyphens. All fixed: 39/39 edge case tests pass, 40/40 unit tests pass.

---
**Category:** `bug` | **Importance:** 7/10
**Files:** N/A
