---
category: architecture
title: "Git Scan Services \u2014 Realtime Orchestrator Awareness"
importance: 9
tags: []
file_paths: []
created: 2026-07-07T03:03:31.789568+00:00
updated: 2026-07-07T03:03:31.789568+00:00
memory_id: 2d04ef74-d3e6-4746-aeeb-5b18526efcf6
---

# Git Scan Services — Realtime Orchestrator Awareness

orchestrator.py now has scan-services command that checks git log + status on all 13 registered services. monitor.py includes check_services_git() in doctor. Startup workflow updated to include scan-services. --watch flag enables hourly rescanning. All scans stored in memory.db at importance 8 for historical tracking.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
