---
category: bug
title: "Carrier extractor captured sentence fragments"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T19:40:12.790397+00:00
updated: 2026-07-08T19:40:12.790397+00:00
memory_id: e94c86e2-fc49-4b9e-8145-b06261405563
---

# Carrier extractor captured sentence fragments

settle_data_scraping_factory/_common/enrich.py _INSURANCE_RE used greedy IGNORECASE [A-Z] and captured whole sentences as insurance_carrier. 86% (3547/4104) of carrier values were garbage. Fixed with known-carrier registry + strict proper-noun+suffix pattern + is_valid_carrier/clean_carrier validators. clean_carriers.py scrubs existing files.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
