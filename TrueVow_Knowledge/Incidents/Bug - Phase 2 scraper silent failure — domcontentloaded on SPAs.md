---
category: bug
title: "Phase 2 scraper silent failure \u2014 domcontentloaded on SPAs"
importance: 10
tags: []
file_paths: []
created: 2026-07-07T03:44:31.485437+00:00
updated: 2026-07-07T03:44:31.485437+00:00
memory_id: 0df3077e-9f60-4b35-9bce-6332f0b35040
---

# Phase 2 scraper silent failure — domcontentloaded on SPAs

CA and FL PI scrapers both used wait_until=domcontentloaded (fires before JS renders). Law firm sites are React/Gatsby/Next.js SPAs — scraper got empty shells. CA: 0% enrichment from 1,850 sites. FL: results never persisted. Root cause: domcontentloaded fires before JS execution on modern SPAs. Fix: Replaced with wait_until=load + networkidle + asyncio.sleep(2) + retry + thin-page detection + Sentry error capture. Also replaced except Exception: pass with proper logging. Added scripts/health_check.py for pre-Supabase data integrity validation. Both scrapers need re-run.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
