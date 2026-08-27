# Phase 3 — State Migration Assurance

**Phase:** 3 of 5
**Authority:** CTO-Knowledge-Orchestrator (assurance only — does not own Sales Ops business decisions)
**Prerequisite:** Gate 0R closed

---

## Decision

**CONDITIONAL APPROVAL**

State migration is approved subject to the conditions below. The migration inventory, legacy mappings, and transition rules are frozen and ready. Migration 177 must pass all dry-run acceptance criteria before production execution.

---

## 1. Migration Inventory

### Source Column

```sql
sales_leads.pipeline_stage TEXT (no CHECK or ENUM constraint)
```

Currently allows 25+ distinct string values. After migration, restricted to canonical states via CHECK constraint.

### Target Constraint

```sql
ALTER TABLE sales_leads ADD CONSTRAINT chk_pipeline_stage_canonical
CHECK (pipeline_stage IN (
  'DISCOVERED','NORMALIZED','PROFILED','CONTACT_ENRICHED',
  'VALIDATION_PENDING','VERIFIED','REJECTED',
  'SCORED','QA_PENDING','REMEDIATION_REQUIRED',
  'OUTREACH_APPROVED','CAMPAIGN_ELIGIBLE','IN_CAMPAIGN',
  'ENGAGED','UNRESPONSIVE','SUPPRESSED',
  'APPLICATION_STARTED','APPLICATION_SUBMITTED','QUALIFICATION_REVIEW',
  'APPROVED_CUSTOMER','REJECTED_CUSTOMER','HANDOFF_PENDING','HANDED_OFF','FAILED'
));
```

### Legacy Value Disposition

| Category | Count | Action |
|---|---|---|
| Direct migrate (identical meaning) | 14 | `UPDATE pipeline_stage = <canonical>` |
| Rename + migrate (same meaning, different name) | 10 | `UPDATE pipeline_stage = <renamed_canonical>` |
| Demote to metadata attribute | 8 | Move to JSONB metadata column; set closest canonical |
| Demote to activity/substate | 6 | Move to `sales_activities` or flag column; set closest canonical |
| Remove (legacy CRM, no current meaning) | 6 | `UPDATE pipeline_stage = <closest_canonical_fallback>` |

**Complete mapping in:** `docs/ontology/legacy_state_mapping.yaml` (44 entries with fallback rules)

### Unmapped-Record Disposition

Any value not in the 44-entry mapping is treated as:

```sql
-- Catch-all: unknown values become FAILED with metadata preservation
UPDATE sales_leads SET
  pipeline_stage = 'FAILED',
  metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
    'migration_unknown_pipeline_stage', pipeline_stage,
    'migration_timestamp', NOW(),
    'migration_migration_id', '177'
  )
WHERE pipeline_stage NOT IN (<all_canonical_values>)
  AND pipeline_stage NOT IN (<all_mapped_legacy_values>);
```

---

## 2. Migration 177 — Dry-Run Requirements

### Pre-conditions

- [ ] Production database backup completed and verified
- [ ] Legacy `pipeline_stage` DISTINCT values audited against mapping
- [ ] 0 records with unmapped values (or explicit disposition approved)
- [ ] Migration SQL reviewed by Sales Ops owner
- [ ] CTO approval of this document

### Dry-Run Steps

```sql
-- Step 1: Count current state
SELECT pipeline_stage, COUNT(*) FROM sales_leads GROUP BY pipeline_stage ORDER BY COUNT(*) DESC;

-- Step 2: Preview migration (dry-run — no commits)
BEGIN;
  -- Execute all UPDATE statements from legacy_state_mapping.yaml
  -- Run catch-all for unmapped values
  -- Re-count by canonical state
  SELECT pipeline_stage, COUNT(*) FROM sales_leads GROUP BY pipeline_stage ORDER BY COUNT(*) DESC;
ROLLBACK;

-- Step 3: Verify constraint will accept all values
BEGIN;
  -- Execute all UPDATEs
  -- Test constraint: ALTER TABLE sales_leads ADD CONSTRAINT ... NOT VALID
  -- Validate constraint: ALTER TABLE sales_leads VALIDATE CONSTRAINT ...
  -- If any row fails, that row's legacy value is undocumented → fix mapping
ROLLBACK;

-- Step 4: Full dry-run with counts
-- Expect: total row count unchanged, no NULL pipeline_stage, all values in canonical set
```

### Acceptance Criteria

- [ ] Total row count before == total row count after
- [ ] 0 rows with NULL pipeline_stage after migration
- [ ] 0 rows with unmapped legacy values in pipeline_stage column
- [ ] All rows map to canonical states or FAILED with preserved metadata
- [ ] CHECK constraint validates all rows
- [ ] Unmapped records have original value preserved in metadata column

---

## 3. Batch and Restart Behavior

### Batch Configuration

```sql
-- Migrate in batches of 10,000 to avoid long-running transactions
-- Each batch is an independent transaction
-- Failed batches can be retried independently
```

### Idempotency

Migration 177 is idempotent — running it twice on the same data produces the same result:

- `UPDATE ... WHERE pipeline_stage = <legacy>` skips already-migrated rows
- Catch-all only targets unmapped values (already-migrated rows are in canonical set)
- No destructive operations (no DELETE, no DROP, no TRUNCATE)

### Rollback

Rollback is a new migration that reverses the mapping:

```sql
-- Reverse migration: canonical → best-guess legacy value
-- Stored in migration metadata for emergency rollback
-- Does NOT guarantee exact original values (demoted-to-metadata values are in JSONB, not pipeline_stage)
```

The CHECK constraint is dropped during rollback and re-added after forward migration completes.

---

## 4. Transition Enforcement

After migration, state transitions must be validated at the application layer.

### Current State

- `PipelineStateManager` in `lib/lead-factory/pipeline-state.ts` validates transitions for `PipelineStage` enum only
- `LeadFunnelStage` type has no transition validation
- Python scripts have no transition validation

### Required Before Production Migration

- [ ] `PipelineStateManager` extended to validate canonical states from `sales_transition_registry.yaml`
- [ ] API route validators check transitions on PATCH/PUT
- [ ] Python scripts check transitions before writing to DB
- [ ] DB trigger rejects invalid transitions at the database level

### DB Trigger (Recommended)

```sql
CREATE OR REPLACE FUNCTION enforce_sales_lead_transitions()
RETURNS TRIGGER AS $$
BEGIN
  -- Load transitions from sales_transition_registry at init
  -- Reject if (OLD.pipeline_stage, NEW.pipeline_stage) not in allowed_transitions
  -- Allow if OLD is NULL (insert)
  -- Allow within FAILED or REMEDIATION_REQUIRED states
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 5. Approval-Evidence Requirements

Before production execution, provide:

- [ ] DISTINCT `pipeline_stage` count from production DB
- [ ] Dry-run output showing all legacy values map to canonical states
- [ ] Row counts: before, after, unmapped, NULL count
- [ ] Sample of 10 rows per migration category (direct, rename, demote, remove, catch-all)
- [ ] CHECK constraint validation PASS
- [ ] Rollback migration tested in staging
- [ ] Sales Ops owner approval of mapping decisions
- [ ] CTO approval of this document

---

## 6. Conditions for Approval

1. **No silent defaults to successful states.** Every record that cannot be definitively mapped must go to `FAILED` with its original value preserved in metadata, not to `DISCOVERED` or `APPROVED_CUSTOMER`.

2. **Dry-run must show total reconciliation.** Row count before must equal row count after. No records silently dropped, duplicated, or corrupted.

3. **Unmapped values must be documented.** If dry-run reveals pipeline_stage values not in the 44-entry mapping, add them to the mapping before proceeding — do not silently catch-all.

4. **Rollback must be tested in staging.** A failed migration must be recoverable without data loss.

5. **Transition enforcement must be in place before migration.** Migrating to canonical states without transition validation creates a window where invalid state changes can be written — worse than the current unconstrained column because it gives a false sense of validation.
