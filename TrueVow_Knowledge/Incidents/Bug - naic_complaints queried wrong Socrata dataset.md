---
category: bug
title: "naic_complaints queried wrong Socrata dataset"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T19:40:14.198851+00:00
updated: 2026-07-08T19:40:14.198851+00:00
memory_id: 92f5785f-8ded-40f8-bca7-f4f9059fcaef
---

# naic_complaints queried wrong Socrata dataset

scripts/scraping-factory/insurance-carrier/naic_complaints.py filtered by 'naic' column on the raw records dataset jjc8-mxkg which has NO carrier column (HTTP 400). Fixed to use complaint-index dataset pa9u-9s9w with naic_id/year/col1-3. Verified real data.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
