---
category: architecture
title: "RETAINER Fly.io deployment verified \u2014 production path proven"
importance: 9
tags: []
file_paths: []
created: 2026-08-01T03:32:25.754083+00:00
updated: 2026-08-01T03:32:25.754083+00:00
memory_id: c11e385f-1b3e-428d-a058-9c3369ccac9c
---

# RETAINER Fly.io deployment verified — production path proven

RETAINER Dockerfile: Python 3.11-slim, uvicorn port 8080, health check at /health. Fly.io config: internal_port 8080, IAD region, 512MB. Secrets: DATABASE_URL, WEBHOOK_KEYS (JSON string parsed via webhook_keys_raw). Dependencies: retainer_contracts installed from local packages dir. Key fix: pydantic-settings Field type changed from dict to str for WEBHOOK_KEYS compatibility. TRACE runs on same region (IAD) with same Supabase pooler — connectivity proven.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
