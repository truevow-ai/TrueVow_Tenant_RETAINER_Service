---
category: decision
title: "FSM Authority Boundary \u2014 state_version"
importance: 10
tags: []
file_paths: []
created: 2026-08-06T17:28:48.856786+00:00
updated: 2026-08-06T17:28:48.856786+00:00
memory_id: 38cefbfd-95d9-4e0c-8233-abb026937797
---

# FSM Authority Boundary — state_version

FSMEngine.transition() is the sole state mutation authority. The ingress processor reads state_version from FSM after transition, never calculates independently. Added FSMEngine.state_version property (derives from transition history). Direct state_version arithmetic in processor verified absent via AST inspection. Commit 891eec8.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
