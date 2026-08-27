---
category: bug
title: "Deploy gate never blocked on RED \u2014 truth-loop.py always exited 0"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T07:11:54.628189+00:00
updated: 2026-07-08T07:11:54.628189+00:00
memory_id: f28746d2-412f-4278-89c9-48dfd4c0f5b6
---

# Deploy gate never blocked on RED — truth-loop.py always exited 0

truth-loop.py __main__ called truth_loop() but never set an exit code, so it always returned 0. orchestrator.py _deploy_service gated on 'if returncode != 0', meaning the gated deployment NEVER actually blocked a FAILED service. Fixed: __main__ now sys.exit(1) on FAILED/skipped and sys.exit(0) only on GREEN (and --all exits 1 if any service FAILED). Verified: GREEN->0, unknown-service->1. Also root-caused SETTLE truth-loop 'hang' to a corrupted 0-byte global ruff.exe shim (repaired via pip force-reinstall), NOT a code fault.

---
**Category:** `bug` | **Importance:** 8/10
**Files:** N/A
