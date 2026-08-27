---
category: bug
title: "Marketing Intelligence null crash"
importance: 7
tags: []
file_paths: []
created: 2026-08-10T15:42:44.533390+00:00
updated: 2026-08-10T15:42:44.533390+00:00
memory_id: 5b8367f5-0f20-49cd-bcde-47eb7210a2a0
---

# Marketing Intelligence null crash

MarketingIntelligence.tsx called toUpperCase() on undefined marketing_activity_level. Fixed with hasValidData guard, optional chaining on score.factors. API now returns valid default structure (overall_score: 0, marketing_activity_level: none).

---
**Category:** `bug` | **Importance:** 7/10
**Files:** N/A
