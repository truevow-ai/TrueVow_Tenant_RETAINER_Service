---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/observability-and-instrumentation/SKILL.md
imported: 2026-08-12T17:53:12.183115+00:00
skill_name: observability-and-instrumentation
---

---
name: observability-and-instrumentation
description: TrueVow platform telemetry — SigNoz, Sentry, OpenTelemetry. Use with /diagnosing-bugs for production investigations.
---

# /observability-and-instrumentation

TrueVow-specific telemetry. Use alongside `/diagnosing-bugs` — the Pocock skill provides the investigation loop; this skill provides the platform telemetry sources.

## Platform Stack

| Layer | Tool | URL |
|-------|------|-----|
| Tracing | SigNoz (OTLP) | `http://localhost:3301` |
| Errors | Sentry | Per-service DSN |
| Metrics | OpenTelemetry → SigNoz | Port 4317 |
| Logs | Fly logs + SigNoz | `fly logs -a <app>` |
| Alerts | Sentry alerts + SigNoz dashboards | — |

## Per-Service OTEL Config

```env
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_SERVICE_NAME=<ServiceName>
```

All 11 services wired. Verify with:
```bash
python TrueVow_Shared_Orchestration/orchestrator.py scan-services
```

## Investigation Pattern

```
/diagnosing-bugs (Pocock)
  ├── Build feedback loop that goes red on this bug
  ├── Minimise reproduction
  ├── Hypothesise root cause
  ├── Instrument: check /observability-and-instrumentation
  │     ├── SigNoz traces — find the failing span
  │     ├── Sentry — check error grouping + frequency
  │     ├── Fly logs — `fly logs -a <app>` for recent crashes
  │     └── Supabase logs — query latency, connection errors
  ├── Fix
  └── Regression-test
```

## Key Metrics

- **P99 latency** per endpoint (SigNoz)
- **Error rate** per service (Sentry)
- **DB connection pool** saturation (Supabase dashboard)
- **Fly machine health** — `fly status`

## Adding Instrumentation

1. Import OpenTelemetry SDK
2. Add span for every external call (DB, HTTP, webhook)
3. Add span attributes: `tenant_id`, `correlation_id`, `command_id`
4. Never log: PHI, secrets, raw stack traces in production

## Related
- `/diagnosing-bugs` — investigation loop (use together)
- `/performance-optimization` — Core Web Vitals + Lighthouse
- `/security-and-hardening` — error exposure rules
