---
category: bug
title: "Sentry DSN Placeholder \u2014 Dashboard Lied"
importance: 10
tags: []
file_paths: []
created: 2026-07-07T05:13:24.787216+00:00
updated: 2026-07-07T05:13:24.787216+00:00
memory_id: 7f6e6156-2bc8-4e91-967f-63bdd01d2ade
---

# Sentry DSN Placeholder — Dashboard Lied

Dashboard previously reported 'Observability: RUNNING' implying Sentry was active. In reality, shared-libraries/sentry/setup-python.py writes # SENTRY_DSN=<add-your-dsn> — a commented placeholder — to every service's .env.local. The Sentry SDK is installed but no real DSN means zero error tracking ecosystem-wide. Fixed: dashboard now scans all 13 services for real DSN values and reports 'MISSING (no real DSN in any service)'. To enable: create a Sentry project, get a DSN, and set SENTRY_DSN=<real-value> in each service's .env.local.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
