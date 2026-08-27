---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/browser-testing-with-devtools/SKILL.md
imported: 2026-08-12T17:53:11.282635+00:00
skill_name: browser-testing-with-devtools
---

---
name: browser-testing-with-devtools
description: Real browser debugging with Chrome DevTools. Use with /diagnosing-bugs for web-specific issues.
---

# /browser-testing-with-devtools

Real browser debugging for TrueVow frontends. Use alongside `/diagnosing-bugs` (Pocock) — that skill provides the structured investigation loop; this skill provides the browser tooling.

## Quick Checks

| Symptom | DevTools Tab | What to Check |
|---------|-------------|---------------|
| Page won't load | Network | 4xx/5xx responses, CORS errors |
| Data not showing | Network → Fetch/XHR | API response body, auth headers |
| UI looks wrong | Elements | Computed styles, layout |
| Click does nothing | Console | JS errors, event listeners |
| Slow page | Performance | Flame graph, long tasks |
| Memory leak | Memory | Heap snapshots over time |
| Auth failure | Application → Cookies | `sb-access-token` present, not expired |

## TrueVow-Specific

- **Sales Ops**: cookie `sb-access-token=canary-session` for staging auth
- **SaaS Admin**: Supabase session in cookies, check `X-Auth-Domain: supabase-iam`
- **Customer Portal**: Clerk session, tenant-scoped queries

## Investigation Pattern

```
/diagnosing-bugs (Pocock)
  └── web-specific bug
       ├── /browser-testing-with-devtools
       │     ├── Reproduce → Network tab → identify failing request
       │     ├── Console → JS errors + stack traces
       │     ├── Application → cookies, localStorage, session
       │     └── Elements → DOM state for UI bugs
       └── Fix → verify in browser → regression-test
```

## Related
- `/diagnosing-bugs` — investigation loop
- `/performance-optimization` — Lighthouse audits
- `/observability-and-instrumentation` — backend telemetry
