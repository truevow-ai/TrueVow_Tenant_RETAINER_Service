---
category: decision
title: "TV-PR-SECRETS-02A-RA: Staging credential risk accepted"
importance: 8
tags: ["security", "risk-acceptance", "staging"]
file_paths: []
created: 2026-08-05T20:13:40.119622+00:00
updated: 2026-08-05T20:13:40.119622+00:00
memory_id: 569a5fd0-7d83-4f92-8793-1e4fd1f62ec5
---

# TV-PR-SECRETS-02A-RA: Staging credential risk accepted

Two active credentials (Sales Ops DB password, DeepSeek API key) remain in private git history but are removed from current tracked tree. Rotations deferred per platform owner authorization. Compensating controls: branches clean, repo private, secret scanning enabled, DB logs reviewed, DeepSeek usage monitored. Rotations required before production GO. Expiration: before PLATFORM-E2E-01 or final GO.

---
**Category:** `decision` | **Importance:** 8/10
**Files:** N/A
