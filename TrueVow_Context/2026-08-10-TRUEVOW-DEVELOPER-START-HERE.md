# TrueVow Developer Start Here

> **v4.0** — 2026-08-24 · THE canonical developer guide. One of exactly three living documents (this guide, `CTO-ORCHESTRATOR-V2-SPEC.md`, `CONTEXT.md`).
> **Living-document rule:** update THIS file in place every session; never fork it; never create a competing guide. Old overlapping docs get a SUPERSEDED banner pointing here.
> Source of truth order when sources conflict: runtime/git state → `memory.db` → this guide → everything else.
>
> **Principle:** the AI is disposable; this context is the durable asset. Point any agent at `TrueVow_Context/` and it becomes the TrueVow CTO's second brain.

---

## 1. What TrueVow Is

TrueVow is an AI-native SaaS platform for **personal-injury (PI) law firms**. It runs the pre-litigation pipeline end to end so a solo attorney — no paralegal, no IT support — can do work that used to take a team.

### Product Doctrine

**INTAKE captures, RETAINER engages, TRACE develops, SETTLE resolves, COMMAND measures.**

| Product | Job |
|---|---|
| **INTAKE** | AI voice intake ("Benjamin") captures and qualifies the injured caller |
| **RETAINER** | Representation review, conflict clearance, engagement packages & signatures |
| **TRACE** | Medical-record retrieval + source-cited treatment chronology |
| **SETTLE** | Attorney-owned settlement database — data-backed settlement ranges |
| **COMMAND** | Measurement layer across the pipeline |
| Supporting | LEVERAGE (zero-knowledge document validation), VERIFY (blockchain certificates), Customer Portal |

### The Three-Portal Model

| Portal | Trust | Users | Products |
|--------|-------|-------|----------|
| **Tenant** (App 3) | EXTERNAL | Law firms + their clients | INTAKE, RETAINER, Customer Portal, TRACE, SETTLE, COMMAND, LEVERAGE, VERIFY |
| **Sales Support** (App 2) | MEDIUM (LLM zone) | Sales operators | Sales Ops |
| **Platform Operators** (App 1) | HIGH (internal) | TrueVow staff + CSM | SaaS Admin, Billing, Internal Ops, Customer Success CORE, Financial Management |

---

## 2. The Golden Journey

```
Website submission / prospect discovery
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
 → Billing / INTAKE / Portal provisioning   [INTAKE provisioning: G11]
 → controlled activation                    [G14 — HARD HOLD]
 → product usage: INTAKE captures → RETAINER engages → TRACE develops
   → SETTLE resolves → COMMAND measures
 → revenue assurance                        [G15]
```

`PLATFORM-E2E-01` is retained as prior commissioning evidence only.

---

## 3. Authoritative Cross-Service Flow

```
PROSPECTING: Sales Ops ──(HMAC handoff)──▶ COMMISSIONING AUTHORITY: SaaS Admin
SaaS Admin ──authoritative onboarding assignment──▶ CSM Core
CSM Core ──readiness evidence──▶ SaaS Admin executes commissioning
SaaS Admin ──▶ Tenant ACTIVE/TRIAL ──provisioning──▶ INTAKE (G11)
```

**No direct Sales Ops → CSM commissioning. No CSM → tenant creation/activation/cancellation.**
SaaS Admin owns authoritative customer identity, tenant lifecycle, and commissioning decisions.

---

## 4. Service Registry

> ⚠️ Ports rot fast. Treat ports as hints and run
> `python TrueVow_Shared_Orchestration/orchestrator.py scan-services` for live truth.

| Service | Repo | Owner | Notes |
|---|---|---|---|
| SaaS Admin | TrueVow_SaaS_Administration_Service | Ghulam Ghous (ISB) | MDM control plane, frozen at PLG-SA-04A |
| Sales Ops | TrueVow_Sales_Ops_Service | Ms. Sania | Pipeline + handoff; had uncommitted work Aug 23 |
| INTAKE | TrueVow_Tenant_INTAKE_Service | Ghulam Ghaus (FSD) | ex-"Tenant Application Service"; Benjamin engine home |
| RETAINER | TrueVow_Tenant_RETAINER_Service | FSD | v1.0 complete, Fly-deployed |
| TRACE | TrueVow_Tenant_TRACE_Service | Yasha | FND-001→003 hardening Aug 18–21 |
| SETTLE | TrueVow_Tenant_SETTLE-Service | Yasha | idle since Aug 12 |
| Billing | TrueVow-Tenant_Billing-Service | FSD | commercial engine; uncommitted work Aug 23 |
| COMMAND | TrueVow_Tenant_COMMAND_Service | Yasha | measurement layer — newest service |
| Customer Portal | Truevow_Tenant_Customer_Portal_Service | Yasha | frontend-only state |
| Customer Success CORE | TrueVow_Customer_Success_CORE_Service | ISB | orchestrates onboarding evidence |
| First Line Support | TrueVow_First_Line_Support_Service | ISB | |
| Financial Mgmt | TrueVow_Financial_Management_Service | Yasha | back-office GL; separated from Billing |
| Internal Ops / Analytics / LEVERAGE / VERIFY / Website | respective repos | Yasha | supporting |
| Shared | TrueVow_Shared_Orchestration · TrueVow_Shared_Codebase_Memory · TrueVow_Shared_Agent_Tools · shared-libraries · TrueVow_Context | all | the ecosystem itself |

Archived/dead: CONNECT (deleted), Dialogflow Intake (dead).

---

## 5. Ownership (Canonical Writer)

| Service | Owns (authoritative minter) | Never does |
|---|---|---|
| **SaaS Admin** | tenant_id, customer_id, contact_id, case_id, tenant lifecycle, commissioning decisions | — |
| **Sales Ops** | lead_id, application_id, pipeline stages, handoff packages | Create tenants; commission CSM directly |
| **CSM Core** | CSM-local projections, onboarding workflows, readiness evidence | Create/activate/cancel tenants, mint tenant_id |
| **Billing** | subscription_id, invoice_id, payment records | — |
| **INTAKE** | intake_session_id, transcripts, qualification | Bill, activate tenants |
| **RETAINER** | representation review, engagement packages, signatures | Mint case_id |
| **TRACE** | matter development, chronology, demand packages | Mint case_id |
| **COMMAND** | cross-pipeline measurement | Mutate business state |
| All others | see prior table (unchanged) | — |

No service mints an ID owned by another service. Correlation chain:
lead_id → application_id → handoff_package_id → handoff_id → customer_id → contact_id → tenant_id → onboarding_run_id → subscription_id → intake_session_id → matter_id.

---

## 6. Binding Platform Invariants

1. SaaS Admin MDM is the only minter of `case_id`.
2. **Auth = Supabase Auth, sole human IdP platform-wide.** Clerk is retired
   (migration completed across services per IAM completion report, 2026-08-03).
   Any Clerk reference in older docs is stale.
3. RULE 0 — no fabrication. Report only what you directly observed. Simulation is
   not commissioning evidence.
4. Mandatory orchestrator check-in protocol (§9).
5. Secrets never touch git; `.env.example` with placeholders only.
6. Tenant isolation at three layers (firm-scope + API validation + Supabase RLS).
7. Migrations are permanent (Alembic, reversible `downgrade()`); INTAKE migrations go
   through Platform Operations governance (`platform-operations/intake_migrate.py`),
   never auto-applied by the app.
8. Observability = SigNoz + Sentry + OpenTelemetry.
9. No external command may be recorded as successfully delivered unless its
   authoritative external effect actually occurred (v3.1 invariant 16).
10. Security credentials are purpose-bound — per-link key isolation (v3.1 invariant 17).
11. Requesting an authoritative action does not transfer authority (v3.1 invariant 18).
12. **Hygiene Rule:** repos with uncommitted changes are frozen for new assignments
    until classified COMMIT / PARK / DISCARD; discard requires explicit founder verb.
13. Commands are intentions; events are facts. A queued command is not a fact.

---

## 7. The CTO Orchestrator

The orchestrator (`TrueVow_CTO_Knowledge_Orchestrator`) is the standing CTO seat:
it runs the Decision Map → Tickets → Briefs loop over all repos, works while the
founder is away, and stops only for HITL gates (dangerous ops, platform questions).

- Spec: `TrueVow_CTO_Knowledge_Orchestrator/CTO-ORCHESTRATOR-V2-SPEC.md`
- Glossary: `TrueVow_CTO_Knowledge_Orchestrator/CONTEXT.md`
- Goal tree: `TrueVow_CTO_Knowledge_Orchestrator/Decision-Map.md`; work units in
  `Tickets/TICKET-*.md` (status lives in each ticket header).
- **Run the cycle:** `python TrueVow_Shared_Orchestration/cto_v2.py shift`
  (status → board refresh → ready-tickets → founder report), or schedule
  `night-shift.bat`. Repo agents receive briefs at `<repo>/docs/work-orders/`;
  end reports with the cited `TICKET:` id.
- Gate ladders are distinct — see glossary before using "Gate" or "G13" language.

---

## 8. Current Platform State (dated snapshot)

> **This section must be refreshed every session that touches any repo. Stale
> snapshots are defects. Last updated: 2026-08-24.**

- **Benjamin engine:** single-path Schema/Goal + LiveKit LIVE ON STAGING
  (LEGACY-RETIREMENT-05 executed ~Aug 14). Google Calendar booking deployed (v1.5.0,
  08C/08C1). Story-latency PASS. Simulation semantic safety gate PASS.
- **G-ladder:** G10 CLOSED · G11 CONDITIONAL/OPEN (5 closure items) · **G13 HOLD**
  (manual testing incomplete as of 2026-08-21) · G14 HARD HOLD · production default NO.
- **TRACE:** FND-001→003 fixes Aug 18–21 (Postgres-only, PHI key fail-closed + re-key,
  RLS reconciliation); 27 uncommitted files at last scan.
- **Sales Ops:** no commits after Aug 13; **58 uncommitted files** — hygiene-frozen.
- **Billing:** no commits after Aug 12; **36 uncommitted files** — hygiene-frozen.
- **SETTLE:** idle since Aug 12, clean.
- **Website:** doctrine sweep Aug 17–19; compliance noindex pending legal/browser QA;
  Benjamin ad landing retired.
- **Staging health:** last measured 4/5 healthy with INTAKE DB connectivity unresolved
  from Fly "personal" org (TV-PR-PHASE-01E, Aug 5) — re-verify before trusting.
- **Known doc debts:** incident TV-PR-INTAKE-MIGRATION-RECOVERY-01 reviewer still
  Pending; Phase-5 commissioning NOT COMMISSIONED.

---

## 9. Session Bootstrap (Every Agent, Every Session)

```
python TrueVow_Shared_Orchestration/orchestrator.py sync-memory
python TrueVow_Shared_Orchestration/orchestrator.py scan-services
python TrueVow_Shared_Orchestration/cto_v2.py status        # hygiene freeze check
python TrueVow_Shared_Orchestration/orchestrator.py dispatch "<task>"
python TrueVow_Shared_Orchestration/orchestrator.py agent-checkin start "<service>: <task> | goal: <success>"
```

End of session:

```
agent-checkin done ... ; memory.py remember <category> "<title>" "<content>" --importance N
python TrueVow_Shared_Orchestration/orchestrator.py push-memory
```

Then: refresh §8 above if anything changed; update board/tickets if the orchestrator
spec is active. **A task is not done until the check-in is posted. Intent is not completion.**

## 10. Engineering Standards & Stack

Boring is a feature. Type everything; handle every error path; test before done.
Attorney-facing UI = plain English, never raw errors. Secrets never touch git.
RULE 0 always.
Stack: Python 3.11 + FastAPI + SQLAlchemy + Alembic; Supabase Postgres (+ Auth);
Next.js/TypeScript; Fly.io; OpenTelemetry → SigNoz + Sentry.

## 11. Stop Conditions

Any binding invariant violated · duplicate cross-service path · minting another
service's ID · secrets/PHI/raw errors to browser · INTAKE voice saying dollar
amounts, case-strength evaluations, or urgency tactics (UPL risk) · TRACE faxing PHI
to an unauthorized provider · SETTLE presenting a range as a guarantee · double-charge
from missing idempotency key · editing a posted journal entry.

---

_Revised v4.0 2026-08-24 — orchestrator realignment, auth correction, registry refresh.
Maintained by the CTO Knowledge Orchestrator._
