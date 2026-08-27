---
category: decision
title: "Transfer Re-engagement: contact_early not contact_info"
importance: 8
tags: []
file_paths: []
created: 2026-08-01T03:49:23.554734+00:00
updated: 2026-08-01T03:49:23.554734+00:00
memory_id: ca21610a-8574-4074-89cb-d67b0b03c7ff
---

# Transfer Re-engagement: contact_early not contact_info

When caller says 'speak to attorney', the global _detect_transfer_request fires and routes to _build_transfer_response. This used contact_info_sequence (end-of-path) which jumped to intake_summary. Fixed to use contact_early_sequence (phone+name) which routes to route_to_ladder → identify_practice_area. contact_early guard added to skip when name+phone already captured. route_to_ladder changed from conflict_check_prior_rep to identify_practice_area. Story lock at IPA now routes to conflict_check_prior_rep instead of direct jurisdiction. Global transfer guard prevents re-trigger after contact captured.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
