# Canonical Decisions (Binding)

> Binding across all services. Each item links to its source of truth. Violating one is a defect. Recall live detail with `python TrueVow_Shared_Orchestration/memory.py recall "<topic>"`.

### 1. Platform Identity & ID Contract — ADR-005 (APPROVED; migration pending)
The canonical identifiers, binding on every service:

| Entity | Canonical ID | Type | Source of truth |
|---|---|---|---|
| Firm | `clerk_org_id` | TEXT (`org_*`) | Clerk |
| User | `clerk_user_id` | TEXT (`user_*`) | Clerk |
| Case | `mdm_cases.case_id` | UUID | **SaaS Admin MDM — the only minter** |
| Client | `contact_id` | UUID | SaaS Admin MDM (`mdm_contacts`) |
| CRM matter | `crm_matter_id` | TEXT | SaaS Admin CRM sync |

Rules: no service mints `case_id` except MDM; firm id is **TEXT, never UUID-cast**; `contact_id` travels alongside TRACE's opaque `client_token` (the non-PHI cross-service client key); `mdm_events_outbox` fans INTAKE → MDM → downstream. **Source:** `TrueVow_Tenant_TRACE_Service/docs/00-Planning/ADR-005-Platform-Identity-and-ID-Contract.md`. TRACE migration + sibling SETTLE/Billing/INTAKE ADRs are pending.

### 2. Auth = Clerk (3-domain). No Supabase Auth migration.
Frontends consume the shared `@truevow/auth-client` (`ClerkWrapper`); backends verify the Clerk JWT and normalize to a `AuthContext(user_id, firm_id, role, permissions)`. Services consume `AuthContext`, **never raw Clerk objects**. **Source:** ADR-003, `shared-libraries/auth-client`.

### 3. RULE 0 — No fabrication (platform-wide)
Never report a build, a test count, or a metric you did not actually produce. If a command did not run green in front of you, it is not green. A stub result is not a real result. **Source:** SETTLE decision memory (RULE 0).

### 4. Mandatory orchestrator check-in protocol
Every session: `sync-memory` → `scan-services` → `agent-checkin start` → work → `remember` → `agent-checkin done` → `push-memory`. A task is not done until the check-in is posted. Without it a service shows `NEGLECTED` and the CTO is blind. **Source:** per-service coding-instructions ("Report to the Orchestrator") + root `AGENTS.md`.

### 5. TRACE stack locks (ADR-003 / ADR-004)
Fax = **Documo**; clinical NER = **OpenMed**; OCR = **PaddleOCR-VL 1.5** (Tier 1B) + **Docling** (Tier 1A) — **deepdoctection ELIMINATED**; **Mistral OCR** = Tier 2 escalation; billing LLM = **Azure GPT-4o-mini**; e-signing = **DocuSeal**. `OCR_CLOUD_BACKEND` locks after the handwriting-spike WER result.

### 6. Product renames / retirements
DRAFT → **LEVERAGE** (same service, renamed). **CONNECT** archived. **First-Line Support** replaced by Chatwoot. **Dialogflow Intake** dead. **Source:** decision memory (importance 10).

### 7. Observability = SigNoz + Sentry + OpenTelemetry
Unified across services. **Source:** architecture memory (importance 10).

### 8. Domain safety invariants
- **LEVERAGE:** zero-knowledge — document content never leaves the attorney's device (not even in logs/telemetry).
- **SETTLE:** bar-compliant anonymization — no client identifiers, ever.
- **INTAKE:** zero-PHI hot path + prohibited-phrase filter — the voice agent may never say a dollar amount, a case-strength evaluation, legal advice, or urgency tactics (UPL risk).
- **TRACE / all tenant health data:** PHI never in logs or URLs; tenant isolation at three layers.
**Source:** per-service `docs/00-Planning/*-Agent-Coding-Instructions.md`.

### 9. Secrets Management — Infisical (Self-Hosted)
Secrets are injected at runtime; `.env.local` does not exist in CI or production. Infisical (self-hosted on TrueVow infrastructure, MIT license) is the single source of truth for all keys, API tokens, and credentials across the platform. Rules: no duplicated secrets across services (one leaked `.env.local` = cross-service compromise); per-trust-domain scoping (App2 never holds App1/App3 secrets); every developer sees only secrets for their owned services (least privilege); a pre-commit hook catches committed secrets; rotation is logged. **Source:** `infisical/README.md`.

_Curated 2026-07-10. Updated 2026-08-10._

### 10. Cross-Service Authority Model (G10 Canary)
The ONLY authorized commissioning path is: **Sales Ops → SaaS Admin → CSM**. No direct Sales Ops → CSM commissioning. No CSM → tenant creation. SaaS Admin owns authoritative customer identity, onboarding state, tenant lifecycle, and commissioning decisions. CSM supplies onboarding/readiness evidence only. **Source:** G10 canary execution, `TV-PR-ONTOLOGY-CROSS-SERVICE-REALIGNMENT-01`.

### 11. SaaS Admin /tenants/internal — REJECTED
`POST /api/v1/tenants/internal` was proposed by SaaS Admin agent but **rejected as canonical architecture**. CSM must not directly create tenants. The file was deleted before deployment. **Source:** CTO decision, session 2026-08-10.

### 12. Service-to-Service Authentication Contract
Cross-service webhooks must use: key ID + timestamp + HTTP method + canonical path + SHA-256(body) + HMAC + clock-skew guard + replay guard. Per-service key isolation (e.g., `tv-sales-ops-to-saas-admin-v1`). Do NOT use generic `X-API-Key` or `X-Service-Name` headers for canonical contracts. **Source:** Sales Ops → SaaS Admin HMAC implementation, CSM 02A hardening.

### 13. Protected Characteristic Inference — FROZEN
The Sales Ops architecture doc describes `special_cohort_leads`, `community_signals`, and ethnicity-based segmentation. Protected/sensitive characteristic inference MUST NOT automatically determine outreach eligibility, pricing, approval, product access, or customer treatment. Frozen for architecture/compliance review before real prospecting at scale. **Source:** CTO directive, session 2026-08-10.

### 14. Trial-to-Paid Conversion — Canonical Commercial Lifecycle
Trial activates automatically after onboarding: **90 days or 12 completed intake sessions, whichever comes first.** Firm may select a paid plan at any time during trial (`plan_selected_at`) but the paid plan does NOT activate until trial exhaustion (`trial_ends_at`). Paid subscription activates atomically (`paid_subscription_activated_at`) with no service interruption. Three distinct timestamps. Trial entitlement is authoritative until trial ends. Optional immediate activation allowed only with explicit customer confirmation (surrenders remaining trial). An "intake" = completed Benjamin intake session reaching defined completion point, not raw inbound call. **Source:** CTO product decision, session 2026-08-10.

### 15. Trial Meter Definition
The trial meter consumes 1 unit per completed Benjamin intake session. Inbound calls that are spam, hang-ups, or otherwise incomplete do NOT consume trial intakes. Monthly call allowances (40/100/200) apply only after paid activation. Billing and INTAKE must share an exact canonical definition of "completed intake session" before commissioning the trial meter. **Source:** CTO product decision, session 2026-08-10.

### 16. Benjamin Architecture — Schema-Gated Intake Engine (North Star)
The final Benjamin conversation architecture is: **talk naturally, collect against a schema, decide against deterministic policy, execute only through validated effects.** Lifecycle shrinks to ~8 states (BOOTSTRAP, SCREENING, INTAKE, RESOLUTION, AWAITING_EFFECT, COMPLETE + HANDOFF, TERMINATED). Facts and goals replace questions and states. LLM chooses HOW to converse within the permitted agenda; code determines the agenda. One caller sentence may satisfy multiple fact requirements — never re-ask. LiveKit is the voice runtime only, not a second orchestration framework. **Not authorized for large implementation yet** — a bounded challenger prototype (Car Accident + OPI) must beat the current vNext on measured conversation quality before any migration. **Source:** CTO research pass, session 2026-08-12.
