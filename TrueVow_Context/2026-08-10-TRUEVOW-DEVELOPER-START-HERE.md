# TrueVow Developer Start Here

> **v3.1** — 2026-08-10  
> The first platform-wide document every developer reads.  
> Source of truth: `TrueVow_Context/`, `canonical-decisions.md`, `memory.db`, per-service `docs/00-Planning/*-Agent-Coding-Instructions.md`.
>
> **Principle:** the AI is disposable; this context is the durable asset. Point any agent at `TrueVow_Context/` and it becomes the TrueVow CTO's second brain without re-explaining the platform.

---

## 1. What TrueVow Is

TrueVow is an AI-native SaaS platform for **personal-injury (PI) law firms**. It runs the pre-litigation intelligence pipeline end to end so a solo attorney — no paralegal, no IT support — can do work that used to take a team.

### The Three-Portal Model

| Portal | Trust | Users | Products |
|--------|-------|-------|----------|
| **Tenant** (App 3) | EXTERNAL | Law firms + their clients | INTAKE, Customer Portal, TRACE, SETTLE, LEVERAGE, VERIFY |
| **Sales Support** (App 2) | MEDIUM (LLM zone) | Sales operators | Sales Ops |
| **Platform Operators** (App 1) | HIGH (internal) | TrueVow staff + CSM | SaaS Admin, Billing, Internal Ops, Customer Success CORE, Financial Management |

### The Product Pipeline — Capture → Build → Protect

- **INTAKE** *(Capture)* — AI voice intake captures the injured caller, qualifies and grades the lead, routes it to the firm.
- **TRACE** *(Build)* — automates medical-record retrieval and builds a demand-ready, source-cited treatment chronology.
- **SETTLE** *(Protect)* — an ethical, attorney-owned settlement database giving data-backed settlement ranges.

Supporting: **LEVERAGE** (zero-knowledge document validation), **VERIFY** (blockchain certificates), **Customer Portal** (attorney dashboard).

### Who We Serve

The **frightened injured person on a phone** and the **solo PI attorney** who stakes their reputation on our output in front of adjusters, judges, and their own client.

---

## 2. The Prospect-to-Revenue Golden Journey

The canonical customer lifecycle, end to end:

```
Prospect discovery
 → normalization / canonical identity
 → enrichment
 → classification
 → governed campaign
 → real engagement
 → demo
 → application
 → human approval (T020)
 → Sales Ops T022 (HANDOFF_PENDING)
 → durable HMAC handoff (tv-sales-ops-to-saas-admin-v1)
 → SaaS Admin authoritative commissioning (fn_process_handoff)
 → onboarding run
 → CSM customer-success onboarding
 → Billing / INTAKE / Portal provisioning
 → controlled activation
 → product usage
 → revenue assurance
 → support
 → offboarding
```

`PLATFORM-E2E-01` is retained as prior commissioning evidence only. The Golden Journey above is the current canonical model.

---

## 3. Authoritative Cross-Service Flow

```
PROSPECTING
══════════════
Sales Ops
    │
    ▼
Human approval — T020
    │
    ▼
Sales Ops → SaaS Admin (HMAC handoff)
    │
    ▼

COMMISSIONING AUTHORITY
═══════════════════════
SaaS Admin
    │ authoritative onboarding assignment
    ▼
CSM Core
    │ customer-success onboarding
    │ readiness / interventions / evidence
    ▼
SaaS Admin (authoritative commissioning)
    │
    ▼
Tenant ACTIVE / TRIAL
```

**No direct Sales Ops → CSM commissioning. No CSM → tenant creation. No CSM → activation.** SaaS Admin owns the authoritative customer identity, tenant lifecycle, and commissioning decisions.

---

## 4. Service Ownership (Canonical Writer)

| Service | Owns (authoritative minter) | Reads | Never does |
|---------|---------------------------|-------|------------|
| **SaaS Admin** | `tenant_id`, `customer_id`, `contact_id`, `case_id`, tenant lifecycle, onboarding state, commissioning decisions | Sales Ops handoff | — |
| **Sales Ops** | `lead_id`, `application_id`, pipeline stages, handoff packages | — | Create tenants, commission CSM directly |
| **CSM Core** | CSM-local projection: `crm_contacts`, onboarding workflows, engagement scores, readiness evidence, scheduling state | SaaS Admin (tenant/customer identity) | Create/activate/cancel tenants, mint `tenant_id`, approve custom intake |
| **Billing** | `subscription_id`, `invoice_id`, payment records | SaaS Admin (tenant identity) | — |
| **INTAKE** | `intake_session_id`, voice transcripts, lead qualification | — | Bill, activate tenants |
| **Customer Portal** | Portal UI state (frontend-only) | All tenant products | Store authoritative business state |
| **TRACE** | `matter_id`, chronology, demand packages | SaaS Admin (case identity) | — |
| **SETTLE** | Settlement ranges, anonymized comparables | — | — |
| **LEVERAGE** | Compliance validation results (zero-knowledge) | — | Store document content |
| **VERIFY** | Blockchain certificates | — | — |
| **Internal Ops** | HR, payroll, RevOps | — | Touch tenant PHI |
| **Financial Mgmt** | General ledger, journal entries | Billing | Edit posted entries |
| **Platform Analytics** | Aggregated metrics, dashboards | All services (read-only) | Mutate business state |

---

## 5. Repository-Reading Method

1. Read `<Service>/docs/00-Planning/<Service>-Agent-Coding-Instructions.md` first. It opens with "The One Thing That Matters Most" and "What Constitutes Failure."
2. Read `<Service>/AGENTS.md` for repo-specific rules.
3. For CSM specifically, read in order:
   - `TrueVow_Customer_Success_CORE_Service/docs/DEVELOPER_GUIDE.md`
   - `TrueVow_Customer_Success_CORE_Service/docs/CSM_CORE_ARCHITECTURE.md`
   - `TrueVow_Customer_Success_CORE_Service/CSM-ONTOLOGY-DELTA.md`
4. Read `TrueVow_Context/canonical-decisions.md` for binding platform-wide rules.
5. Run `python TrueVow_Shared_Orchestration/orchestrator.py scan-services` for real-time git state.

---

## 6. Binding Platform Invariants

### Existing (from canonical-decisions.md)

1. SaaS Admin MDM is the only minter of `case_id`.
2. Auth = Clerk (3-domain). No Supabase Auth migration.
3. RULE 0 — no fabrication.
4. Mandatory orchestrator check-in protocol.
5. Secrets never touch git; `.env.example` with placeholders only.
6. Tenant isolation at three layers (firm-scope + API validation + Supabase RLS).
7. Migrations are permanent (Alembic, reversible `downgrade()`).
8. Observability = SigNoz + Sentry + OpenTelemetry.

### New (from ontology/canary commissioning, 2026-08-10)

**16. No external command may be recorded as successfully delivered unless its authoritative external effect actually occurred.**  
Prevents `DELIVERY_MODE=disabled → DELIVERED → SUCCEEDED` defects. Transport suppression is not delivery. Simulation is not commissioning evidence.

**17. Security credentials are purpose-bound.**  
Do not reuse another service's API key, webhook secret, or signing secret for an unrelated capability. Per-service key isolation with distinct key identities (`tv-sales-ops-to-saas-admin-v1`, etc.).

**18. Requesting an authoritative action does not transfer authority.**  
A service may recommend or request an authoritative action; calling the authoritative service's API does not make the caller the authority. The canonical owning service retains decision rights.

---

## 7. Command/Event Semantics

Commands are intentions; events are facts.

**Extended semantics (v3.1):**
- A command is not a fact merely because it was queued.
- A delivery is not successful merely because transport was suppressed.
- An event must represent an effect that actually occurred.
- Simulation output is not commissioning evidence.

The canonical service-to-service contract uses:
```
key ID + timestamp + HTTP method + canonical path + SHA-256(body) + HMAC + clock-skew guard + replay guard + idempotency
```

---

## 8. Correlation Identifiers (Journey Tracking)

When tracking a customer through the Golden Journey, these IDs form the audit chain:

```
lead_id
application_id
handoff_package_id
handoff_id
customer_id
contact_id
tenant_id
onboarding_run_id
platform_command_id
csm_contact_id
```

Then continuing through provisioning:
```
subscription_id
intake_session_id
matter_id
portal_session_id
```

No service mints an ID owned by another service.

---

## 9. Cross-Service Integration Warnings

### ACTIVE AND BINDING

```
Sales Ops → SaaS Admin
Canonical path: POST /api/v1/webhooks/sales-ops/application-approved
Auth: HMAC-SHA256 (tv-sales-ops-to-saas-admin-v1)
Status: COMMISSIONED (G10 canary in progress)
```

### PENDING (DO NOT BUILD AGAINST)

```
SaaS Admin → CSM canonical onboarding contract
Work order: TV-PR-SAAS-CSM-ONTOLOGY-CONTRACT-01
Status: PENDING — not yet implemented

Legacy /api/v1/customers/transfer
Status: NOT CANONICAL
DO NOT BUILD NEW INTEGRATIONS AGAINST IT
```

---

## 10. Stop Conditions — When to Halt Work

### General
- A proposed change violates any binding canonical decision.
- A new cross-service path duplicates an existing canonical contract.
- A service is asked to mint an ID owned by another service.
- Secrets, PHI, or raw stack traces would leak to the browser.

### CSM-Specific
- CSM is asked to mint a `tenant_id`.
- CSM is asked to create, activate, or cancel a tenant.
- CSM confidence scoring is being used to grant platform authority.
- A new Sales Ops → CSM commissioning path appears.
- New code targets legacy `POST /api/v1/customers/transfer`.
- A cross-service event/command is being invented outside the ontology registry.

### Domain-Specific
- **INTAKE:** the voice agent says a dollar amount, case-strength evaluation, or urgency tactic (UPL risk).
- **TRACE:** a misdirected fax sends PHI to an unauthorized provider.
- **SETTLE:** a settlement range is presented as a guarantee.
- **LEVERAGE:** document content leaves the attorney's device.
- **Billing:** a missing idempotency key double-charges a tenant.
- **Financial Management:** a posted journal entry is edited in place.

---

## 11. Session Bootstrap (Every Agent, Every Session)

```
python TrueVow_Shared_Orchestration/orchestrator.py sync-memory
python TrueVow_Shared_Orchestration/orchestrator.py scan-services
python TrueVow_Shared_Orchestration/orchestrator.py dispatch "<task>"
python TrueVow_Shared_Orchestration/orchestrator.py agent-checkin start "<service>: <task> | goal: <what success looks like>"
```

End of session:
```
python TrueVow_Shared_Orchestration/orchestrator.py agent-checkin done "<service>: <done> | outcome | learned | next" --status DONE
python TrueVow_Shared_Orchestration/memory.py remember <category> "<title>" "<content>" --importance N
python TrueVow_Shared_Orchestration/orchestrator.py push-memory
```

**A task is not done until the check-in is posted. Intent is not completion.**

---

## 12. Engineering Standards

- Boring is a feature. Simple is not simplistic. Write it twice before you abstract.
- Type everything; handle every error path; write the test before calling it done.
- Attorney-facing UI = plain English. Never show HTTP codes, stack traces, `null`/`undefined`, or JSON.
- Loading/empty states are instructions, not spinners.
- Secrets never touch git. Per-trust-domain scoping. Pre-commit hook catches committed secrets.
- **RULE 0 — no fabrication.** Report only what you directly observed.

---

## 13. Standard Stack

Python 3.11 + FastAPI + async SQLAlchemy + Alembic; Supabase Postgres (+ Storage); Next.js/TypeScript frontends; Fly.io hosting; Clerk auth (3-domain); OpenTelemetry → SigNoz + Sentry observability.

---

## 14. Documentation Updates

- Regenerate memory digest: `python TrueVow_Shared_Orchestration/memory.py export`
- Sync Obsidian vault: `python TrueVow_Shared_Orchestration/obsidian-bridge.py`
- Recall live detail: `python TrueVow_Shared_Orchestration/memory.py recall "<topic>"`

---

_Curated 2026-07-10. Revised v3.1 2026-08-10 — ontology/canary realignment.  
Maintained by the CTO Knowledge Orchestrator._
