# Incident Report: TV-PR-INTAKE-MIGRATION-RECOVERY-01

## Summary

Unauthorized staging schema mutation caused by a disposable test isolation failure.
The frozen migration `20260805_add_request_receipts` was applied to the staging
`public` schema instead of the disposable `_migration_test_02` schema.

## Incident ID

`TV-PR-INTAKE-MIGRATION-RECOVERY-01`

## Timeline (UTC)

| Time | Event |
|------|-------|
| 02:10Z | `rehearsal2.py` created disposable schema `_migration_test_02` |
| 02:10Z | Frozen migration SQL executed without `SET search_path` |
| 02:10Z | `ALTER TABLE intake_sessions ADD state_version` committed to `public` |
| 02:10Z | `CREATE TABLE intake_request_receipts` committed to `public` |
| 02:10Z | Verification query targeted `_migration_test_02` — appeared to fail |
| 02:19Z | CTO post-mortem discovered `state_version` in `public` schema |
| 02:19Z | Migration activity frozen, forensic snapshot taken |
| 02:25Z | Catalog-definition parity confirmed: exact match to frozen migration |
| 02:30Z | Governance metadata recorded (RECONCILED_UNAUTHORIZED_APPLY) |

## Root Cause

The rehearsal script `rehearsal2.py` created a disposable test schema but
did not execute `SET search_path` before running the frozen migration SQL.
The unqualified DDL statements (`ALTER TABLE intake_sessions`, `CREATE TABLE`)
targeted the default connection schema (`public`) instead of the disposable
`_migration_test_02` schema.

**Contributing factor:** `psycopg2` was configured with `autocommit=True`,
meaning each DDL statement committed independently. There was no transaction
boundary to roll back.

## Affected Objects

- `public.intake_sessions.state_version` (BIGINT NOT NULL DEFAULT 0)
- `public.intake_sessions.ck_state_version_non_negative` (CHECK)
- `public.intake_sessions.uq_intake_sessions_tenant_session` (UNIQUE)
- `public.intake_request_receipts` (21 columns, 5 constraints, 5 indexes, RLS)
- `public.platform_schema_migrations` (empty ledger)
- `public.platform_schema_migration_attempts` (empty attempt history)

## Data Impact

- 42 sessions initialized to `state_version = 0` (correct default)
- 0 receipt rows created
- 0 session data changes
- 0 business data corruption

## Catalog-Definition Parity

All expected objects from the frozen migration match the actual staging schema:
columns, types, nullability, defaults, check constraints, unique constraints,
foreign keys, indexes, RLS policies, and grants.

## Recovery

The schema was determined to be an exact match to the frozen migration.
No data was corrupted. The staging state was accepted as reconciled.

A success-ledger row was inserted manually by the CTO operator with
`application_mode = RECONCILED_UNAUTHORIZED_APPLY` and
`incident_id = TV-PR-INTAKE-MIGRATION-RECOVERY-01`.

An attempt-history row was inserted with `status = RECONCILED`,
`error_classification = DISPOSABLE_ISOLATION_FAILURE`, and
`reconstructed = true`.

## Manual Action Disclosure

The success-ledger row was inserted via manual SQL by the CTO operator.
No governed `reconcile` command was available at the time of recovery.
The `reconcile` command was subsequently implemented in the committed runner.

## Preventive Controls

1. Physically separate disposable database required for all migration tests
2. Target guards reject staging identity in disposable/test mode
3. `verify` command is read-only (zero writes)
4. `reconcile` requires explicit incident ID and human confirmation
5. Ledger records `application_mode` to distinguish governed vs reconciled
6. Attempt history preserves failure/interruption provenance

## Operator

CTO Knowledge Orchestrator / Platform Operations

## Reviewer

Pending
