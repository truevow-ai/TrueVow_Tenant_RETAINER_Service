---
category: bug
title: "Gitignore Source-Leak FIXED \u2014 All 6 services"
importance: 10
tags: []
file_paths: []
created: 2026-07-01T01:16:07.575317+00:00
updated: 2026-07-01T01:16:07.575317+00:00
memory_id: f97c11af-0137-4939-8dd1-cbee6b827114
---

# Gitignore Source-Leak FIXED — All 6 services

All 6 affected services now have anchored .gitignore patterns. lib/, env/, venv/, build/, dist/ now use leading / to prevent accidental source file hiding. Leaked PowerShell commands removed from FM, Billing, and LEVERAGE. SETTLE test_db_conn.py and recover_pyc.py anchored to root only. Internal Ops, SETTLE, and LEVERAGE latent rules also fixed.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
