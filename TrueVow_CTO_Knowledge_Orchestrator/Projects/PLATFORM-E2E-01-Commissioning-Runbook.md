# PLATFORM-E2E-01 — Master Commissioning Runbook

> **Date**: 2026-08-04
> **Status**: Code phases frozen. Platform Operations commissioning required.

---

## Service Release State

| Service | Frozen Commit | Branch | Tree | Deployed Staging? |
|---------|--------------|--------|------|-------------------|
| **SaaS Admin** | `8c67516` → `1cb75ba` | saasadmin/iam-supabase-auth | CLEAN | YES (v29, staging) |
| **INTAKE** | `57f05ae` | main | CLEAN | NO — migrations + template seed pending |
| **Sales Ops** | `92330b5` (v26) | main | DIRTY (78 files) | PENDING |
| **Tenant Billing** | Commercial-statement refactor committed | feat branch | DIRTY (161 files) | PENDING — needs release freeze |
| **Financial Management** | `3f587e5` | feat/customer-finance-module | CLEAN (CF files) | PENDING — HMAC key needed |

---

## Gate 1 — Environment Preflight (Platform Operations)

| # | Check | Status |
|---|-------|--------|
| 1 | SaaS Admin clean deploy at `8c67516` | READY |
| 2 | INTAKE frozen at `57f05ae` | READY (code only) |
| 3 | FM frozen at `3f587e5` | READY (code only) |
| 4 | Billing commercial-statement refactor committed | NEEDS RELEASE FREEZE |
| 5 | Sales Ops clean state | NEEDS COMMIT (78 dirty) |

---

## Gate 2 — INTAKE Commissioning (PLG-INTAKE-01R-E)

**Action**: Platform Operations

### 2.1 — Apply SQL Migrations

Go to `TrueVow_Tenant_INTAKE_Service/operations/database/migrations/`

| # | File | Action |
|---|------|--------|
| 1 | `20260803_add_workflow_path_to_template_versions.sql` | Apply to staging DB |
| 2 | `20260803_seed_pi_standard_intake_template.sql` | Apply to staging DB |

### 2.2 — Resolve Schema Drift

Code queries 6 columns on `tenant_configurations` that may not exist in DDL:

```
retain_transcripts, retain_audio, retention_days,
consent_signed_date, firm_name, firm_email
```

Add the missing columns if they don't exist.

### 2.3 — Verify

```sql
SELECT template_code, template_version, checksum, workflow_path
FROM intake_template_versions
WHERE template_version = '1.0.0';
```

Required: 64-character SHA-256 checksum present. Template `PI_STANDARD_INTAKE` active.

### 2.4 — Deploy INTAKE

```
Commit: 57f05ae
Deploy to INTAKE staging
```

---

## Gate 3 — SaaS Admin → INTAKE (PLG-SA-04B)

**Prerequisites**: SaaS Admin staging deployed at `8c67516`, INTAKE staging deployed at `57f05ae`

### Tests

1. SaaS Admin provisions synthetic tenant → POST `/api/v1/internal/tenants/provision`
2. INTAKE returns acknowledgment
3. Replay same command → duplicate acknowledgment
4. Changed checksum → 409 conflict
5. INTAKE validates template checksum
6. INTAKE uses shared engine factory (0 direct `OakwoodIntakeWorkflowEngine` constructions)

---

## Gate 4 — Customer Acquisition to Live INTAKE

**Prerequisites**: Gate 2 + 3 PASS

Synthetic law-firm journey:

```
1. Sales Ops application → approved
2. SaaS Admin creates tenant (exactly once)
3. Contact identity preserved
4. Onboarding state progresses correctly
5. INTAKE template = PI_STANDARD_INTAKE v1.0.0
6. No raw workflow JSON crosses service boundaries
7. CSM review recorded
8. Test call evidence attached
9. SaaS Admin activates tenant (only SaaS Admin performs activation)
```

### Negative proofs

```
Duplicate tenant: 0
Oakwood branding in new tenant: 0
Direct INTAKE DB access from SaaS Admin: 0
```

---

## Gate 5 — Controlled INTAKE Call

**Prerequisites**: Gate 4 PASS

```
1. Correct tenant resolved
2. Correct firm name used (not Oakwood)
3. Active configuration resolved
4. Checksum validated
5. Shared engine factory used
6. Workflow progresses
7. Session closes normally
8. Canonical outbox record created
```

### Negative proofs

```
Unknown tenant → fail closed
Inactive tenant → fail closed
Invalid checksum → fail closed
Missing configuration → fail closed
V2_SKIP_LLM=true → call succeeds without LLM
V2_SKIP_LLM=false → call succeeds with LLM
```

---

## Gate 6 — Test Isolation

Synthetic journey must NOT produce:

```
production campaign enrollment: 0
production customer notifications: 0
commercial trial increment: 0
billable usage increment: 0
real payment attempt: 0
real provider webhook: 0
```

---

## Gate 7 — Billing → FM Handshake

**Prerequisites**: Billing release freeze, FM deployed at `3f587e5`

```
1. Configure FM_HMAC_KEY on both Billing staging and FM staging
2. Billing in CUSTOMER_FINANCE_AUTHORITY=BILLING_LEGACY
3. Billing finalizes synthetic CommercialStatementFinalized (25 fields)
4. Billing dispatches to FM
5. FM returns accepted acknowledgment
6. Billing marks dispatch ACKNOWLEDGED
```

### Replay

```
Identical replay → duplicate acknowledgment
Changed replay → 409 conflict
Response loss → retry → duplicate → ACKNOWLEDGED
```

### Zero side effects

```
FM invoices: 0, FM payments: 0, FM journals: 0
```

---

## Gate 8 — Cross-Service ID Traceability

Every transition must be traceable:

```
application_id → tenant_id → contact_id → onboarding_id
→ provisioning_command_id → configuration_version
→ INTAKE session_id → test-call evidence ID
→ operational entitlement ID → commercial_statement_id
→ FM acknowledgment_id → correlation_id
```

No service may query another's database directly.

---

## Gate 9 — Failure Paths

| Failure | Expected |
|---------|----------|
| Duplicate application approval | No duplicate tenant |
| Provisioning timeout | Retry or review state |
| INTAKE unavailable | No silent fallback |
| INTAKE accepts but response lost | Retry → duplicate ack |
| Invalid HMAC | Denied |
| Changed replay | 409 conflict |
| Inactive template | Rejected |
| Checksum mismatch | Rejected |
| Test call failure | Evidence attached, no activation |
| Activation before readiness | Rejected |
| FM unavailable | Billing retry, no dead-letter |
| FM duplicate statement | Duplicate acknowledgment |
| FM changed-checksum | 409 conflict |

For every failure: no duplicate records, no silent fallback, no cross-service DB write, correct retry/review state.

---

## Final Acceptance

```
Acquisition-to-activation journey:          PASS
Controlled tenant-specific call:            PASS
SaaS Admin → INTAKE commissioning:          PASS
Billing → FM acknowledgment round-trip:     PASS
Duplicate canonical records:                0
Cross-service database writes:              0
Silent fallbacks:                           0
Unauthorized lifecycle transitions:         0
Oakwood branding leakage:                   0
Unresolved critical/high-severity defects:  0
```
