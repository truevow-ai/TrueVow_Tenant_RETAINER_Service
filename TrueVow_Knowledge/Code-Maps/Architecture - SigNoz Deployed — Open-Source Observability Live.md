---
category: architecture
title: "SigNoz Deployed \u2014 Open-Source Observability Live"
importance: 10
tags: []
file_paths: []
created: 2026-07-07T06:45:52.121766+00:00
updated: 2026-07-07T06:45:52.121766+00:00
memory_id: 0b938497-d0db-474f-9b18-ff7e0a705796
---

# SigNoz Deployed — Open-Source Observability Live

SigNoz (open-source Datadog alternative) deployed as the TrueVow observability stack. Replaces the non-functional Sentry placeholder (# SENTRY_DSN=<add-your-dsn>). Stack: 5 Docker containers running (OTEL Collector on :4317/:4318, ClickHouse for traces/metrics, Query Service on :8080, Frontend UI on :3301, Jaeger fallback on :16686). All 11 services wired: setup.py --all copied otel_init.py / otel-node.js to each service, added OTEL_EXPORTER_OTLP_ENDPOINT to .env.local. Dashboard now shows OTEL wired: 11/11 and SigNoz: http://localhost:3301. Benefits: distributed tracing + metrics + error tracking all in one self-hosted platform, no API key needed.

---
**Category:** `architecture` | **Importance:** 10/10
**Files:** N/A
