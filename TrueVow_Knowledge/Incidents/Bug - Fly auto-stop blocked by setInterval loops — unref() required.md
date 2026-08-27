---
category: bug
title: "Fly auto-stop blocked by setInterval loops \u2014 unref() required"
importance: 10
tags: []
file_paths: []
created: 2026-07-23T18:37:46.278081+00:00
updated: 2026-07-23T18:37:46.278081+00:00
memory_id: 0f8d60bb-81af-4c20-9c0d-e95a98c2d2b4
---

# Fly auto-stop blocked by setInterval loops — unref() required

CRITICAL: Four server-side setInterval timers in Sales Ops were preventing Fly.io auto-stop from working. The fly.toml had auto_stop_machines = true and min_machines_running = 0, but the machines ran 24/7 because Node.js event loop never drained. Root cause: setInterval creates a timer reference that Node counts as 'pending work'. Fly cannot suspend a machine whose process won't exit.

The four offenders in Sales Ops:
1. Logger — 5s flush interval (lib/utils/logger.ts)
2. SecurityMonitor — 5s anomaly scan (lib/ai-agents/security/security-monitor.ts)
3. RateLimiter — 300s cleanup (lib/middleware/rate-limiter.ts)
4. HeartbeatTask — 300s registry heartbeat (lib/integrations/internal-ops-registry-client.ts)

Fix: Add .unref() to every setInterval call on the server side. This tells Node 'don't consider this timer as keeping the process alive.' The interval still fires while the process is running, but when Fly determines the machine is idle and sends SIGTERM, the process can exit cleanly.

Pattern:
  const interval = setInterval(() => { ... }, ms);
  interval.unref();

AUDIT CHECKLIST for every other TrueVow service deployed on fly.io:
1. Search for ALL setInterval calls in server-side code (not browser/client components)
2. Every one that doesn't already have .unref() MUST get it
3. Pay special attention to: loggers, monitoring loops, health-check pings, cleanup tasks, heartbeat tasks, polling loops
4. Also check: email-verifier/reacher-truevow had NO auto_stop_machines config at all in its fly.toml — it ran 24/7. All fly.toml files need auto_stop_machines = true, auto_start_machines = true, min_machines_running = 0
5. Verify: deploy, wait 10 minutes with no traffic, check 'fly status' — machine should show 'stopped'

Estimated cost impact if unfixed: ~/machine/month for shared-cpu VMs running 24/7 vs ~-5/month with auto-stop.

---
**Category:** `bug` | **Importance:** 10/10
**Files:** N/A
