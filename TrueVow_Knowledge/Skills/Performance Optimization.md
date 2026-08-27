---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/performance-optimization/SKILL.md
imported: 2026-08-12T17:53:12.226069+00:00
skill_name: performance-optimization
---

---
name: performance-optimization
description: TrueVow web performance audit — Core Web Vitals, Lighthouse, rendering anti-patterns. Use with /diagnosing-bugs for performance regressions.
---

# /performance-optimization

Lighthouse-based performance audit for TrueVow frontends. Use alongside `/diagnosing-bugs` for performance regressions — the Pocock skill provides the investigation loop; this skill provides the web performance tooling.

## Audit

Run Lighthouse on the target page:
```bash
npx lighthouse <url> --view --output html --output-path .lighthouse/report.html
```

## TrueVow-Specific Checks

| Metric | Target | Tool |
|--------|--------|------|
| LCP (Largest Contentful Paint) | < 2.5s | Lighthouse |
| FID (First Input Delay) | < 100ms | Lighthouse |
| CLS (Cumulative Layout Shift) | < 0.1 | Lighthouse |
| TTFB (Time to First Byte) | < 800ms | Chrome DevTools Network tab |
| Bundle size | Per-route < 200KB JS | `next build` output |
| DB query latency | < 50ms p50 | SigNoz traces |

## Frontend-Specific

- **Sales Ops:** LeadsList with 2,971 rows — verify virtualization, pagination at 20, no full-table renders
- **Customer Portal:** Tenant-specific bundles, no cross-tenant JS leakage
- **SaaS Admin:** Dashboard queries — check for N+1 patterns

## Investigation Pattern

```
/diagnosing-bugs (Pocock)
  └── performance regression
       ├── /performance-optimization
       │     ├── Lighthouse audit → identify metric violation
       │     ├── Chrome DevTools Performance tab → flame graph
       │     ├── Network tab → slowest requests
       │     └── Bundle analyzer → largest chunks
       └── Fix → re-audit → confirm improvement
```

## Output
- Lighthouse scores (Performance, Accessibility, Best Practices, SEO)
- Top 3 improvement opportunities with estimated impact
- Bundle size regression check (compare with previous build)

## Related
- `/diagnosing-bugs` — investigation loop
- `/observability-and-instrumentation` — SigNoz traces for backend perf
- `/browser-testing-with-devtools` — real browser debugging
