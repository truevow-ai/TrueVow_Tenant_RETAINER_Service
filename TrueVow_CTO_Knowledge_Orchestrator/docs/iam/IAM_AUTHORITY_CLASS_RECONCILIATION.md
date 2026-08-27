# IAM Authority Class Reconciliation Report

**Generated:** 2026-08-02  
**Scope:** Cross-service audit of authority class implementations  
**Author:** CTO Knowledge Orchestrator (automated)  
**Sources inspected:**
- `TrueVow_SaaS_Administration_Service\lib\contracts\index.ts` (432 lines)
- `TrueVow_SaaS_Administration_Service\lib\services\authority-gate-service.ts` (141 lines)
- `TrueVow_SaaS_Administration_Service\lib\api\middleware.ts` (227 lines)
- `TrueVow_SaaS_Administration_Service\lib\auth\scope-middleware.ts` (392 lines)
- `TrueVow_SaaS_Administration_Service\lib\rbac-constants.ts` (428 lines)
- `TrueVow_SaaS_Administration_Service\supabase\migrations\159_authority_gate_framework.sql` (420 lines)
- `TrueVow_SaaS_Administration_Service\supabase\migrations\168_ontology_completion.sql` (343 lines)
- `TrueVow_SaaS_Administration_Service\supabase\migrations\169_contract_normalization.sql` (295 lines)
- `TrueVow_SaaS_Administration_Service\supabase\migrations\179_iam_identity_core_foundation.sql` (234 lines)
- `TrueVow_Sales_Ops_Service\lib\contracts.ts` (147 lines)
- `TrueVow_Sales_Ops_Service\lib\events\event-builder.ts` (89 lines)
- `TrueVow_Sales_Ops_Service\lib\transitions\transition-authority.ts` (170 lines)
- `TrueVow_Sales_Ops_Service\app\api\v1\leads\[id]\handoff-to-saas-admin\route.ts` (195 lines)
- `TrueVow_Documentation\TrueVow_California_RETAINER_Compliance_Decision_Map_v1.0.md` (192 lines)
- All RLS policy and DB gate seed SQL files

---

## 1. CRITICAL FINDING: Two Incompatible Authority Class Vocabularies

There are **two parallel, semantically incompatible authority class systems** in the codebase.

### Vocabulary A: SaaS Admin (Legal Domain) — 6 Frozen Classes

Defined in `TrueVow_SaaS_Administration_Service\lib\contracts\index.ts` (lines 14-21):

| Enum Value | String | Meaning |
|------------|--------|---------|
| `SYS_ADMIN` | `sys_admin` | Platform may execute administrative automation without case-specific human approval |
| `FIRM_POLICY` | `firm_policy` | Execution allowed only under an approved, versioned tenant policy (standing automated rule) |
| `STAFF_AUTH` | `staff_authorized` | A designated, named firm staff member must approve or perform the action (attributed to a specific person) |
| `ATTY_AUTH` | `attorney` | A licensed attorney must decide — the most common gate for legal-judgment actions |
| `CLIENT_AUTH` | `client` | The client must decide or provide informed authorization |
| `PROHIBITED` | `prohibited` | TrueVow must not perform this activity under any automation setting |

### Vocabulary B: Sales Ops Domain — 7+7 Classes (2 forms)

Defined in `TrueVow_Sales_Ops_Service\lib\contracts.ts` (lines 28-33):

| Short Form | Prefixed Form | Semantic Meaning |
|------------|--------------|-----------------|
| `OBSERVE` | `salesops_observe` | Observe only (read-only data access) |
| `RECOMMEND` | `salesops_recommend` | Make recommendations |
| `DRAFT` | `salesops_draft` | Prepare drafts for review |
| `ACT_BOUNDED` | `salesops_act_bounded` | Execute within defined guardrails |
| `APPROVE` | `salesops_approve` | Approve approvals |
| `ADMINISTER` | `salesops_administer` | System administration |
| `NEVER_AUTOMATE` | `salesops_never_automate` | Never automate |

### Vocabulary C: California Compliance Map (Documentation) — 6 Classes

Defined in `TrueVow_California_RETAINER_Compliance_Decision_Map_v1.0.md` (lines 22-28):

| Class | Mapping to SaaS Admin |
|-------|----------------------|
| `AUTO` — Automate | ≈ `SYS_ADMIN` |
| `FIRM` — Firm policy | ≈ `FIRM_POLICY` |
| `ATTY` — Attorney control | ≈ `ATTY_AUTH` |
| `CLIENT` — Client control | ≈ `CLIENT_AUTH` |
| `BLOCK` — Blocked | ≈ `PROHIBITED` |
| `COUNSEL` — Counsel review | No direct equivalent (excluded from v1; future work) |

### Vocabulary D: DB Gate `required_authority` (Migration 159) — Hybrid Set

The `authority_gates.required_authority` CHECK constraint in migration 159 (line 30-33) accepts a **hybrid superset** that does not match either vocabulary:

```
suitable_authority IN (
  sys_admin, firm_policy, staff_authorized, attorney,
  responsible_attorney, managing_attorney,
  compliance_reviewer, client, prohibited
)
```

Note: `responsible_attorney`, `managing_attorney`, and `compliance_reviewer` are **roles**, not authority classes. This was fixed in migration 169 (line 136) which narrowed the CHECK to the 6 canonical SaaS Admin classes. However, the consolidated 155-161 migration (line 211) still has the hybrid CHECK.

---

## 2. INDIVIDUAL AUTHORITY CLASS PROFILES — SaaS Admin (Legal Domain)

### 2.1 SYS_ADMIN (`'sys_admin'`)

**Meaning:** Platform may execute administrative automation without case-specific human approval.

**Governed decisions (code evidence):**
1. `fn_evaluate_authority_gate()` line 274-276: Any gate with `required_authority = 'sys_admin'` immediately returns `{success: true, authority: 'sys_admin'}`
2. `TransitionContract.required_authority` field (contracts/index.ts line 155): Indicates this is a valid assigned authority for state transitions
3. `authority_grants` table (migration 179, line 128): Can be granted as a `SYS_ADMIN` authority class to identity profiles

**Roles that may exercise it:**
- `SUPER_ADMIN` (Level A, Clerk App 1) — has all permissions
- `ADMIN` (Level A, Clerk App 1)
- `TrueVow Platform Actor` (actor ACT-028 in migration 168, `authority_class = 'sys_admin'`)

**Delegable:** No. The DB gate evaluator immediately succeeds without checking delegations or roles. It is an unconditional system pass-through.

**Tenant-scoped:** No. It operates above tenant boundaries. The evaluator does not check `actor_roles` or `tenant_id` for SYS_ADMIN gates.

**Evidence required:** Determined gate-by-gate. Most administrative gates have `audit_required = true` but `evidence_required` may be empty. Authority decisions are always logged to `authority_decisions`.

**Always prohibited operations:** None at this level — SYS_ADMIN is a blanket authorization. However, no gate registered for `legal.judgment`, `representation.accept`, `conflict.clear`, or `settlement.accept` uses SYS_ADMIN.

---

### 2.2 FIRM_POLICY (`'firm_policy'`)

**Meaning:** Execution allowed only under an approved, versioned tenant policy (standing automated rule).

**Governed decisions (code evidence):**
1. `fn_evaluate_authority_gate()` lines 298-307: Checks if actor has any of the required roles. If so, authorizes. If not, returns `{success: true, note: 'Gate deferred to app-layer policy check'}` — meaning it **never denies** in the DB layer.
2. Registered gates using FIRM_POLICY:
   - `template.activate` — Activate approved template (roles: `firm_admin`)
   - `engagement.deliver` — Deliver engagement package (roles: `firm_admin`, `intake_coordinator`)
   - `intake.collect_facts` — Collect factual intake info (roles: `intake_coordinator`, `legal_assistant`, `paralegal`)
   - `intake.classify_practice_area` — Classify practice area (roles: `intake_coordinator`, `responsible_attorney`)
   - `conflict.run_search` — Run conflict search (roles: `intake_coordinator`, `paralegal`, `responsible_attorney`)
   - `data.purge_matter` — Delete confidential matter data (roles: `managing_attorney`, `compliance_reviewer`)
   - `ai.output.accept` — Accept AI output (roles: `firm_admin`, `responsible_attorney`)
3. California compliance map: 8 `FIRM`-classed decisions (A01, A02, A03, A04, A07, A09, B01, B06, etc.)

**Roles that may exercise it:**
- `OWNER`, `BILLING_ADMIN` (Level D, tenant roles)
- `CUSTOMER_SUCCESS`, `CLIENT_ONBOARDING_MANAGER` (Level B, platform operators)
- Any tenant user whose role is in the gate's `required_role` array

**Delegable:** Yes, through `authority_delegations` table (lines 279-296 of `fn_evaluate_authority_gate`). Delegations are checked before role evaluation.

**Tenant-scoped:** Yes. Delegation lookup uses `tenant_id`. The `authority_decisions` table always requires `tenant_id`.

**Evidence required:** Yes, all gates with FIRM_POLICY have `audit_required = true` and `evidence_required` JSONB arrays specifying what must be recorded (e.g., `template_id`, `activation_timestamp`, `jurisdiction_code`)

**Always prohibited operations:** 
- Making legal conclusions from intake data (A10, A11 — `PROHIBITED`/`BLOCK`)
- Representing classification as legal acceptance
- Giving legal advice (A06 — `ATTY_AUTH`)

---

### 2.3 STAFF_AUTH (`'staff_authorized'`)

**Meaning:** A designated, named firm staff member must approve or perform the action (attributed to a specific person).

**Governed decisions (code evidence):**
1. `fn_evaluate_authority_gate()` lines 309-313: Role-based check using `required_role && p_actor_roles` (PostgreSQL array overlap). If actor has any required role, success.
2. No explicitly registered gates in the seeded 15+8 gates that use `staff_authorized` as `required_authority`. However, the CHECK constraint accepts it.
3. Actor definitions in migration 168 map `Intake Coordinator` and `Firm Administrator` to `staff_authorized`.
4. California compliance map: Staff-classed activities prepare records, assemble facts, recommend routing under firm policy (B06).

**Roles that may exercise it:**
- `STAFF` (Level C, Clerk App 2 — LLM Zone)
- `PARALEGAL` (Level D, tenant)
- `ASSISTANT` (Level D, tenant)
- `INTAKE_MANAGER` (tenant role in migration 179)
- `CASE_STAFF` (tenant role in migration 179)

**Delegable:** Yes, through `authority_delegations`. Checked before role evaluation.

**Tenant-scoped:** Yes. Delegation and attribution are always tenant-scoped.

**Evidence required:** Gate-dependent. `audit_required = true` by default. The actor is always attributed.

**Always prohibited operations:**
- Creating the attorney approval event (B06 — requires ATTY_AUTH)
- Drafting or explaining legal consents
- Stating a limitations deadline as legal conclusion (A07)

---

### 2.4 ATTY_AUTH (`'attorney'`)

**Meaning:** A licensed attorney must decide — the most common gate for legal-judgment actions.

**Governed decisions (code evidence):**
1. `fn_evaluate_authority_gate()` lines 309-313: Same role-based overlap check as STAFF_AUTH.
2. Registered gates using ATTY_AUTH:
   - `representation.approve` — Approve representation (roles: `responsible_attorney`, `managing_attorney`)
   - `conflict.clear` — Clear a conflict (roles: `responsible_attorney`, `managing_attorney`, `compliance_reviewer`)
   - `template.approve` — Approve legal template (roles: `responsible_attorney`, `managing_attorney`, `compliance_reviewer`)
   - `matter.activate` — Activate matter (roles: `responsible_attorney`, `managing_attorney`)
   - `settlement.recommend` — Settlement recommendation (roles: `responsible_attorney`, `litigation_attorney`)
   - `lien.resolve` — Lien resolution (roles: `responsible_attorney`)
   - `disbursement.authorize` — Trust disbursement (roles: `managing_attorney`, `firm_admin`)
   - `data.export` — Export confidential data (roles: `managing_attorney`, `firm_admin`)
   - `engagement.explain_terms` — Explain legal effect (roles: `responsible_attorney`, `supervising_attorney`)
   - `matter.deadline_conclusion` — State legal deadline (roles: `responsible_attorney`, `litigation_attorney`)
   - `demand.authorize` — Authorize demand (roles: `responsible_attorney`, `litigation_attorney`)
   - `lien.approve_resolution` — Approve lien resolution (roles: `responsible_attorney`)
3. California compliance map: 7 attor-classed decisions (A06, B03, B04, B05, B07, B10 + all settlement/legal gates)

**Roles that may exercise it:**
- `ATTORNEY` (Level D, tenant)
- `SUPER_ADMIN`, `ADMIN` (Level A — over-scoped but inclusive)
- Actor definitions: ACT-010 (Responsible Attorney), ACT-011 (Supervising Attorney), ACT-012 (Managing Attorney), ACT-013 (Litigation Attorney) — all mapped to `attorney`

**Delegable:** Yes, through `authority_delegations`. Delegation from an attorney to another role (e.g., paralegal) is supported, limited by scope, and expiration.

**Tenant-scoped:** Yes.

**Evidence required:** Yes, all ATTY_AUTH gates require specific evidence (attorney_id, approval_timestamp, document_hash, scope, etc.). `audit_required = true` universally.

**Always prohibited operations:**
- Self-approval (INV-011): AI cannot create authority to approve its own output
- Non-attorney overrides: INV-018 — "Administrative role or tenant ownership never implies attorney authority"
- AI recommending representation acceptance (G11 — BLOCK in CA compliance map)

---

### 2.5 CLIENT_AUTH (`'client'`)

**Meaning:** The client must decide or provide informed authorization. The platform may capture but never substitute for client judgment.

**Governed decisions (code evidence):**
1. `fn_evaluate_authority_gate()` lines 309-313: Same role-based overlap check. However, note that typical client gates have `required_role = NULL` (see `esign.consent`, `engagement.sign`, `settlement.accept`), meaning the DB check for these gates will fall through to denial since there are no roles to match. **These gates must be handled at the app layer** where client authentication is verified differently (e.g., via signed documents, OTP, portal session).
2. Registered gates using CLIENT_AUTH:
   - `esign.consent` — Consent to e-signature (roles: NULL — app-layer enforcement)
   - `engagement.sign` — Sign engagement agreement (roles: NULL — app-layer enforcement)
   - `settlement.accept` — Accept settlement offer (roles: NULL — app-layer enforcement)
3. California compliance map: 4 `CLIENT`-classed decisions (B10, C01, etc.)

**Roles that may exercise it:**
- `CLIENT`, `CLIENT_ADMIN` (Level D, tenant — Clerk App 3)
- Actor definitions: ACT-001 (Prospective Client), ACT-002 (Client) — both mapped to `client`

**Delegable:** Technically yes via `authority_delegations`, but in practice for CA v1, client decisions are non-delegable (settlement authority requires personal informed consent per CA Rule 1.2(a)).

**Tenant-scoped:** Yes.

**Evidence required:** Yes, highly specific:
- `esign.consent`: `person_id`, `consent_version`, `ip_address`, `user_agent`, `timestamp`
- `engagement.sign`: `person_id`, `document_hash`, `signature_intent`, `timestamp`, `authentication_method`
- `settlement.accept`: `client_id`, `offer_id`, `informed_decision_evidence`, `attorney_advice_received`

**Always prohibited operations:**
- Platform signing for client (TV-CMP-009)
- Accepting settlement without client authority (INV-005)
- Substituting for client judgment in any legal commitment

---

### 2.6 PROHIBITED (`'prohibited'`)

**Meaning:** TrueVow must not perform this activity under any automation setting. Reserved exclusively for external actors.

**Governed decisions (code evidence):**
1. `fn_evaluate_authority_gate()` lines 269-271: **Always denies.** Immediate `{success: false, reason: 'Action is prohibited'}`.
2. `authority_class_vocabulary` (migration 169): `platform_may_execute = false`, `example_actors = ['n/a']`
3. `PROHIBITED_PAYLOAD_CONTENT` (contracts/index.ts lines 107-110): Event envelopes must not contain `passwords`, `api_keys`, `oauth_tokens`, `credit_card_numbers`, `ssn`, `full_dob`, `pii_in_clear`
4. `validateEventEnvelope()` (line 253-261): Rejects events with prohibited payload patterns
5. California compliance map: `BLOCK`-classed decisions:
   - A10: Use intake data to train TrueVow models
   - A11: Reuse one firm's intake data for another firm
   - A12: Tell prospect which lawyer/firm to hire
   - B11: Automatically accept a prospect who meets criteria
   - E07: Contact a person who requested no further contact
   - G11: Use AI to recommend accepting/rejecting representation
   - G13: Use agentic AI to send an agreement
6. `EventEnvelope` JSON Schema (line 323-329): `not: { required: [product extension fields] }` — product extensions prohibited at root

**Roles that may exercise it:**
- **None.** This class exists to explicitly block operations. Actor ACT-029 (AI Assistance Component) is mapped to `prohibited`.

**Delegable:** **Never.** The gate evaluator returns `false` before checking delegations.

**Tenant-scoped:** N/A (it denies all, regardless of tenant).

**Evidence required:** N/A (never authorized). Denial is logged to `authority_gate_denials`.

**Always prohibited operations:**
- Any activity assigned PROHIBITED in the authority_gates table
- Secrets in event payloads
- AI creating its own authority path (TV-CMP-015)
- Cross-tenant data pooling
- Automated representation acceptance
- Product extension fields in canonical envelope

---

## 3. INDIVIDUAL AUTHORITY CLASS PROFILES — Sales Ops Domain

These classes are used only within `TrueVow_Sales_Ops_Service` and are **not known** to SaaS Admin, RETAINER, or any other service.

### 3.1 OBSERVE / salesops_observe

**Meaning:** Observe only (read-only data access).

**Governed decisions:** Defined in the type system. No specific enforcement code found in route/middleware.

**Roles that may exercise it:** Any authenticated user with read access (via `requireAuth()`).

**Delegable:** Not modeled.

**Tenant-scoped:** Pre-tenant events use `tenant_id = null` (via `buildPreTenantEvent`). Post-handoff events set tenant_id.

**Evidence required:** No specific evidence checks. Standard event envelope generation.

---

### 3.2 RECOMMEND / salesops_recommend

**Meaning:** Make recommendations (e.g., lead scoring recommendations).

**Governed decisions:** Type-level definition only. No gate evaluation code uses this.

---

### 3.3 DRAFT / salesops_draft

**Meaning:** Prepare drafts for human review (e.g., email template drafts, auto-reply drafts).

**Governed decisions:** Type-level definition only. No gate evaluation code uses this.

---

### 3.4 ACT_BOUNDED / salesops_act_bounded

**Meaning:** Execute within defined guardrails.

**Governed decisions (code evidence):**
1. `transition-authority.ts` line 96: **Every lead state transition** uses `authority_class: 'salesops_act_bounded'` regardless of whether the transition requires human or system actor.
2. `golden-fixtures.ts` line 23: The golden pre-tenant event uses `salesops_act_bounded`.
3. `event-builder.test.ts`: Multiple tests use `salesops_act_bounded` for standard events.

**Actual enforcement:** The `transitionLead()` function enforces `actor` type at line 70-72: if a transition requires `human` actor and `actorType !== 'human'`, it throws `TransitionError('human_required')`. This is a **manual check**, not integrated with the SaaS Admin gate framework.

**Roles that may exercise it:** System, agent, or human actors depending on the transition definition in `TRANSITIONS`.

**Delegable:** Not modeled.

**Tenant-scoped:** Pre-tenant (tenant_id = null) for most transitions; tenant-scoped when `buildEventEnvelope` is used with a valid tenant_id.

**Evidence required:** For specific transitions:
- `APPROVED_CUSTOMER`: requires `approval_decision_id`
- `HANDOFF_PENDING`: requires `handoff_package_id` and `handoff_checksum`

---

### 3.5 APPROVE / salesops_approve

**Meaning:** Approve approvals (e.g., application approval, handoff approval).

**Governed decisions (code evidence):**
1. `handoff-to-saas-admin/route.ts` line 89: The `HandoffPackage.authority_record` uses `authority_class: 'APPROVE'` (short form, not prefixed). Note: this is assigned to `authority_record_id: crypto.randomUUID()` — a **self-generated UUID**, violating INV-011 (no self-approval).
2. `golden-fixtures.ts` line 45: Golden tenant-scoped event (`handoff.completed`) uses `salesops_approve`.
3. Event builder test line 54: Golden tenant-scoped event uses `salesops_approve`.

**Roles:** Human operator (`authorized-operator`, `operator-uuid-12345`).

**Delegable:** Not modeled.

**Tenant-scoped:** Yes (tenant_id is set for post-handoff events).

**Evidence required:** `approval_decision_id` validated in transition evidence.

---

### 3.6 ADMINISTER / salesops_administer

**Meaning:** System-level administration.

**Governed decisions:** Type-level definition only. No gate evaluation code uses this.

---

### 3.7 NEVER_AUTOMATE / salesops_never_automate

**Meaning:** Never automate — equivalent to PROHIBITED in the SaaS Admin vocabulary.

**Governed decisions:** Type-level definition only. No explicit enforcement code found. The `email-template-service.ts` has `prohibited_claims_checklist` for validating templates against forbidden content (lines 306-339): prohibits "AI-powered", "risk-free", superlative words, "guaranteed".

---

## 4. RECONCILIATION TABLE

| SaaS Admin (Legal) | Sales Ops (Sales) | CA Compliance Map | Compatibility |
|-------------------|-------------------|-------------------|--------------|
| `SYS_ADMIN` | `ADMINISTER` | `AUTO` | **Moderate.** Sales Ops ADMINISTER is narrower but same direction. AUTO in CA map maps to administrative execution after objective checks. |
| `FIRM_POLICY` | `ACT_BOUNDED` | `FIRM` | **High.** Both mean "execute within defined policy guardrails." Both rely on named, versioned policy snapshots. |
| `STAFF_AUTH` | `DRAFT` | (embedded in FIRM for staff-prep) | **Low.** DRAFT is narrower (draft only), STAFF_AUTH covers any staff-attributed action. DRAFT has no explicit gate. |
| `ATTY_AUTH` | — | `ATTY` | **Not mapped.** Sales Ops has no attorney concept — pre-tenant, no legal relationship exists. |
| `CLIENT_AUTH` | — | `CLIENT` | **Not mapped.** Sales Ops has no client concept — operates before client exists. |
| `PROHIBITED` | `NEVER_AUTOMATE` | `BLOCK` | **High.** Both mean "platform must not perform." But Sales Ops NEVER_AUTOMATE has no gate framework equivalent. |
| — | `OBSERVE` | — | Sales Ops only — no legal domain equivalent (read-only isn't a legal concern) |
| — | `RECOMMEND` | — | Sales Ops only — recommendations without legal effect |
| — | `APPROVE` | — | Sales Ops only — operational approvals (not legal in nature) |

---

## 5. ENFORCEMENT ARCHITECTURE

### 5.1 SaaS Admin: Three-Layer Enforcement

```
Layer 1: API Middleware (lib/api/middleware.ts, lib/auth/scope-middleware.ts)
  ├── withAuth() — JWT verification (Clerk)
  ├── requireTenantScope() / requireInternalScope() — scope gating  
  ├── withPermission() — RBAC permission check
  └── withRole() — RBAC role check

Layer 2: Authority Gate Service (lib/services/authority-gate-service.ts)
  ├── evaluateGate() — calls fn_evaluate_authority_gate() RPC
  ├── requireGate() — throws 403 on denial
  └── recordDecision() — immutable audit log

Layer 3: Database RLS + Gate Function (PostgreSQL)
  ├── fn_evaluate_authority_gate() — server-side evaluation
  ├── authority_decisions — immutable decisions (trigger-enforced)
  ├── authority_gate_denials — security monitoring
  └── RLS policies on all tenant tables (tenant_own_data, admin_all_access)
```

### 5.2 Sales Ops: Single-Layer Enforcement

```
Layer 1: Route-level guards
  ├── requireAuth() — basic auth bypass (dev mode) or Clerk validation
  ├── transitionLead() manual actor checks (human vs system)
  └── State machine validation (T022, T023 transitions)
  
No authority gate service integration.
No fn_evaluate_authority_gate() calls.
No authority_decisions logging for Sales Ops events.
```

### 5.3 Gap: Sales Ops Does Not Call Authority Gates

The handoff route (`handoff-to-saas-admin/route.ts`) generates `authority_record_id: crypto.randomUUID()` locally without calling `evaluateGate()`. This means:
1. INV-011 (no self-approval) is violated
2. No gate evaluation occurs for `application.approve`
3. No immutable authority decision is recorded in SaaS Admin's `authority_decisions`
4. The authority record is fabricated, not verified

---

## 6. RLS POLICY COVERAGE

From migration 004 (lines 1060-1101):
- 17 tables have RLS enabled
- All have `admin_all_access` policy (system admins see everything via `USING (TRUE)`)
- `tenant_accounts` has `tenant_own_data` policy (tenants see own data via `current_setting('app.current_tenant_id')`)
- Later migrations (114, 116, 179) add more granular tenant-scoped RLS policies

From migration 132 (workflow_rls.sql) — explicit posture: **"ENABLE RLS with NO policies = deny everyone"** for workflow tables. Only `service_role` bypasses RLS.

From migration 179 (IAM foundation) — `authority_grants` table has RLS enabled with `platform_operator_access` policy (all platform operators can read/write).

---

## 7. RECOMMENDATIONS

### 7.1 Vocabulary Reconciliation (PRIORITY: HIGH)
- **Unify or bridge the two authority class systems.** The Sales Ops 14-class vocabulary (7 short + 7 prefixed) is completely disconnected from the SaaS Admin frozen 6-class vocabulary.
- **Option A (preferred):** Map Sales Ops classes to the 6 canonical classes explicitly in a v2 of `contracts.ts`, with a runtime mapper.
- **Option B:** Keep separate vocabularies but document the boundary explicitly as "pre-tenant sales domain" vs "post-activation legal domain."

### 7.2 Gate Integration for Sales Ops (PRIORITY: HIGH)
- Integrate Sales Ops `transitionLead()` to call SaaS Admin's `evaluateGate()` for human-actor transitions (T010, T011, T017, T018, T020, T021, T026).
- For system-actor transitions, record decisions rather than fabricating UUIDs.
- Add `authority_class` to each transition in the registry so authority is configurable, not hardcoded.

### 7.3 Client-Auth Gate Enforcement (PRIORITY: MEDIUM)
- Client gates (esign.consent, engagement.sign, settlement.accept) have `required_role = NULL`, which means `fn_evaluate_authority_gate()` will deny them in the DB layer.
- Build explicit app-layer enforcement for client authentication (portal session, OTP, document signing ceremony).

### 7.4 Self-Approval Protection (PRIORITY: HIGH)
- The handoff route generates its own `authority_record_id` — a self-approval that violates INV-011.
- Replace `crypto.randomUUID()` with a call to `evaluateGate('application.approve', {...})` and `recordDecision(...)`.
- Consider adding a DB-level check that `authority_record_id` references an existing `authority_decisions` row before events are accepted.

### 7.5 Consolidated Migration Fix (PRIORITY: LOW)
- Migration CONSOLIDATED_155_161_RUN_ME.sql (line 211) still has the hybrid CHECK constraint with role names mixed into authority classes. The fix in migration 169 needs to be reflected in the consolidated migration.

---

## 8. APPENDIX: Authority Class Order (from SaaS Admin)

The `AUTHORITY_CLASS_ORDER` array defines the escalation path (contracts/index.ts lines 34-41):

```
SYS_ADMIN → FIRM_POLICY → STAFF_AUTH → ATTY_AUTH → CLIENT_AUTH → PROHIBITED
```

This represents increasing human involvement and decreasing automation capability. Events can only escalate upward (more human, less automated) never downward. This ordering is used by `validateEventEnvelope()` for validation but is not currently enforced as a transition constraint.

---

## 9. APPENDIX: Full Gate Registry

### 9.1 Registered Gates (from migrations 159 + 168)

| Gate Code | Product | Action | Required Authority | Required Roles | Evidence Required | Failure Mode |
|-----------|---------|--------|-------------------|----------------|-------------------|-------------|
| representation.approve | retainer | Approve representation | attorney | responsible_attorney, managing_attorney | attorney_id, approval_timestamp, scope_of_representation | fail_closed |
| conflict.clear | retainer | Clear a conflict | attorney | responsible_attorney, managing_attorney, compliance_reviewer | attorney_id, clearance_rationale, conflict_search_id | fail_closed |
| template.approve | retainer | Approve legal template | attorney | responsible_attorney, managing_attorney, compliance_reviewer | attorney_id, approval_timestamp, document_hash | fail_closed |
| template.activate | retainer | Activate approved template | firm_policy | firm_admin | template_id, activation_timestamp, jurisdiction_code | fail_closed |
| engagement.deliver | retainer | Deliver engagement package | firm_policy | firm_admin, intake_coordinator | template_version, package_hash, delivery_authorization_timestamp | fail_closed |
| esign.consent | retainer | Consent to e-signature | client | NULL | person_id, consent_version, ip_address, user_agent, timestamp | fail_closed |
| engagement.sign | retainer | Sign engagement agreement | client | NULL | person_id, document_hash, signature_intent, timestamp, authentication_method | fail_closed |
| matter.activate | retainer | Activate matter | attorney | responsible_attorney, managing_attorney | attorney_id, activation_checklist_passed, conflict_cleared, agreement_signed, jurisdiction_code | fail_closed |
| settlement.recommend | settle | Settlement recommendation | attorney | responsible_attorney, litigation_attorney | attorney_id, analysis_reference, offer_details | fail_closed |
| settlement.accept | settle | Accept settlement offer | client | NULL | client_id, offer_id, informed_decision_evidence, attorney_advice_received | fail_closed |
| lien.resolve | settle | Approve lien resolution | attorney | responsible_attorney | attorney_id, lien_id, resolution_amount, negotiation_evidence | fail_closed |
| disbursement.authorize | settle | Authorize trust disbursement | attorney | managing_attorney, firm_admin | authorized_by, disbursement_amount, payee_verified, ledger_reconciliation_hash | fail_closed |
| jurisdiction.activate | command | Activate jurisdiction | compliance_reviewer | compliance_reviewer, admin | profile_id, jurisdiction_code, approval_date, counsel_approval | fail_closed |
| ai.output.accept | command | Accept AI output | firm_policy | firm_admin, responsible_attorney | ai_model, input_hash, output_hash, accepted_by, acceptance_timestamp | fail_closed |
| data.export | command | Export confidential data | attorney | managing_attorney, firm_admin | requested_by, export_scope, data_classifications, recipient | fail_closed |
| intake.collect_facts | intake | Collect factual intake info | firm_policy | intake_coordinator, legal_assistant, paralegal | source, raw_response, collected_by, collection_timestamp | fail_closed |
| intake.classify_practice_area | intake | Classify practice area | firm_policy | intake_coordinator, responsible_attorney | classification_source, confidence, reviewed_by | fail_closed |
| conflict.run_search | retainer | Run conflict search | firm_policy | intake_coordinator, paralegal, responsible_attorney | search_input, search_scope, search_timestamp, results_count | fail_closed |
| engagement.explain_terms | retainer | Explain legal effect | attorney | responsible_attorney, supervising_attorney | attorney_id, question_text, response_text, response_timestamp | fail_closed |
| matter.deadline_conclusion | trace | State legal deadline | attorney | responsible_attorney, litigation_attorney | attorney_id, statute_reference, analysis, approval_timestamp | fail_closed |
| demand.authorize | settle | Authorize demand | attorney | responsible_attorney, litigation_attorney | attorney_id, demand_package_hash, authorization_timestamp, jurisdiction_code | fail_closed |
| lien.approve_resolution | settle | Approve lien resolution | attorney | responsible_attorney | attorney_id, lien_id, resolution_amount, negotiation_summary, jurisdiction_code | fail_closed |
| data.purge_matter | command | Delete confidential matter data | firm_policy | managing_attorney, compliance_reviewer | authorized_by, deletion_scope, retention_policy_ref, legal_hold_checked, backup_policy_ref | fail_closed |

**Total:** 23 authority gates, all `fail_closed`. Zero `escalate` or `fail_open_delegated` gates.

---

*End of Report*
