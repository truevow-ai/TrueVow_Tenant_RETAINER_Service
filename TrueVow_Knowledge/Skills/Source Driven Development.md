---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/source-driven-development/SKILL.md
imported: 2026-08-12T17:53:12.452889+00:00
skill_name: source-driven-development
---

---
name: source-driven-development
description: Read before you write. Understand the codebase, ontology, and contracts before implementing. Use /research for external investigation.
---

# /source-driven-development

Read existing code, contracts, and decisions before writing new code. Composes with `/research` (Pocock) for external investigation and `/domain-modeling` (Pocock) for vocabulary.

## Read Order

1. **`TrueVow_Context/START-HERE.md`** — platform overview, binding decisions
2. **`<Service>/docs/00-Planning/<Service>-Agent-Coding-Instructions.md`** — "The One Thing That Matters Most"
3. **`<Service>/AGENTS.md`** — repo-specific rules
4. **Existing code** — grep for similar patterns, read nearby tests
5. **Ontology registry** — check for existing events/commands before inventing new ones

## Rules

- Never fabricate a build, test count, or metric (RULE 0)
- If a fact seems stale, fix the source first, then re-derive
- Cross-service events must go through the ontology registry — never invent locally
- Existing canonical contract takes precedence over convenience

## Session Start

```bash
python TrueVow_Shared_Orchestration/orchestrator.py sync-memory
python TrueVow_Shared_Orchestration/orchestrator.py scan-services
```

## Related
- `/research` — external investigation
- `/domain-modeling` — build shared vocabulary
- `/to-spec` — document findings as a spec
