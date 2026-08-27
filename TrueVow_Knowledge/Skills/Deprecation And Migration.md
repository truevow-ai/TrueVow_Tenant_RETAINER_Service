---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/deprecation-and-migration/SKILL.md
imported: 2026-08-12T17:53:11.646430+00:00
skill_name: deprecation-and-migration
---

---
name: deprecation-and-migration
description: TrueVow-safe data migration and deprecation. reversible downgrade(), never edit applied migrations. Use /to-tickets for migration planning.
---

# /deprecation-and-migration

Safe data and code deprecation. Use `/to-tickets` (Pocock) for migration planning — that skill creates the ticket DAG; this skill adds data safety rules.

## Migration Rules

- **Alembic migrations are permanent** — never edit an applied migration
- **Always write `downgrade()`** — reversible, tested both directions
- **Test with production-like data volume** — not just empty tables
- **New columns:** `ADD COLUMN IF NOT EXISTS` with safe defaults
- **Dropping columns:** soft-deprecate first (stop writing), drop in next migration
- **Schema changes across services:** coordinate via ontology contract, not direct DB access

## Deprecation Pattern

```
1. /to-tickets → plan the deprecation as ticket DAG
2. Mark deprecated in code (comment + CHANGELOG)
3. Stop writes to deprecated path
4. Monitor: zero traffic for N days
5. Remove in next migration
```

## Safety Gates

- Never drop a column that another service reads
- Never change a column type without a transition period
- Run migration on staging first, verify, then production
- Have rollback plan ready before applying

## Related
- `/to-tickets` — plan the migration
- `/shipping-and-launch` — deployment gate
