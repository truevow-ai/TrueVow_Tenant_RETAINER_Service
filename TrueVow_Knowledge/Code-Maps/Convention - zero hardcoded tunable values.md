---
category: convention
title: "zero hardcoded tunable values"
importance: 10
tags: []
file_paths: []
created: 2026-07-15T05:58:55.101384+00:00
updated: 2026-07-15T05:58:55.101384+00:00
memory_id: f6dd35d7-03dc-429a-ada9-39d5b615fc50
---

# zero hardcoded tunable values

RULE: This is a multi-tenant platform. Never hardcode ANY value that may need adjustment per-tenant, per-firm, or per-environment. All tunables must live in one of: (1) tenant_config, (2) workflow JSON config, or (3) named module-level constants with clear documentation. Bare numbers, strings, or IDs in logic statements are FORBIDDEN. If you need a value that could change — threshold, timeout, limit, firm identifier, VAD setting, confidence score — expose it via config. Test by asking: 'Could a different law firm need this set differently?'

---
**Category:** `convention` | **Importance:** 10/10
**Files:** N/A
