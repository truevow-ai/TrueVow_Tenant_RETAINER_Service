---
source: TrueVow_SaaS_Administration_Service/.opencode/skills/qa-mode/SKILL.md
service: TrueVow_SaaS_Administration_Service
type: internal-mdm
stack: ["nextjs", "typescript", "postgresql", "supabase"]
imported: 2026-08-12T17:53:14.733984+00:00
skill_name: qa-mode
---
# SaaS Admin QA Mode

## Service-specific (global verify patterns in truevow-verify)

### Truth commands
```bash
pnpm install && pnpm typecheck && pnpm lint && pnpm build && npx jest --testPathPatterns="tests/"
```

### Lint gate
0 errors required, warnings allowed. `pnpm lint` = `next lint --max-warnings 9999`

### Test baseline
777 passed / 0 failed / 574 skipped (0 failing suites). Any regression = investigate before commit.

### Branching
`git checkout -b feat/<description>` → works? merge to main, delete branch. Breaks? discard, restart.

### NEVER expose .env.local secrets and keys in the IDE chat
