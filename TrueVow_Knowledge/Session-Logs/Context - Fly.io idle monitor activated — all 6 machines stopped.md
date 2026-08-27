---
category: context
title: "Fly.io idle monitor activated \u2014 all 6 machines stopped"
importance: 7
tags: ["fly", "automated", "cost-savings"]
file_paths: []
created: 2026-07-11T15:12:09.165543+00:00
updated: 2026-07-11T15:12:09.165543+00:00
memory_id: 84255da3-af74-4018-bd7e-ae540f1d3676
---

# Fly.io idle monitor activated — all 6 machines stopped

Orchestrator now monitors Fly.io idle machines via monitor_fly_idle.py (checks every 10 min; stops machines idle >30 min). Initial cleanup: stopped 2 machines (intakely-backend + email-outreach-frontend) that had been running with zero activity since June 2 (39 days). All 6 machines across 3 apps (truevow-ai, intakely-backend, email-outreach-frontend) now stopped/suspended. Zero Fly billing until next deploy.

---
**Category:** `context` | **Importance:** 7/10
**Files:** N/A
