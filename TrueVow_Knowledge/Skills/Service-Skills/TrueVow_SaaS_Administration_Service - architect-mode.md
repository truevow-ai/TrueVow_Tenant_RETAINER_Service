---
source: TrueVow_SaaS_Administration_Service/.opencode/skills/architect-mode/SKILL.md
service: TrueVow_SaaS_Administration_Service
type: internal-mdm
stack: ["nextjs", "typescript", "postgresql", "supabase"]
imported: 2026-08-12T17:53:14.624031+00:00
skill_name: architect-mode
---
# SaaS Admin Architect Mode

## Service-specific knowledge only (global patterns in truevow-plan)

### SaaS Admin is the Shared Platform
SaaS Admin hosts governance infrastructure consumed by 5 products:
- Tenant & identity core, Authority gates, Jurisdiction profiles, Firm policies
- Consent ledger, Document service, Communication service, Integration hub
- Portal access grants + invitations, Audit event store

### Product ownership (what lives where)
- **SaaS Admin**: definitions (workflows, templates, gates, policies, jurisdictions, consent, docs, comms, integrations, audit, portal access)
- **INTAKE Service**: execution (workflow_engine.py, intake routing)
- **RETAINER**: engagement (representation decisions, conflicts, packages, signatures)
- **TRACE**: case production (evidence, medical, damages, chronology)
- **SETTLE**: resolution (offers, liens, disbursements, closure)
- **COMMAND**: operations (metrics, SLAs, work items)

### Contract freeze (9 frozen contracts)
- EventEnvelope v1.0.1 (18 fields), MatterActivatedPayload v1.0, ActivationEvidenceManifest v1.0
- WebhookSignature v1.0, AuthorityClass Registry v1.0, Ontology Registry v1.0
- Event Catalog v1.0, Transition Contract v1.0, RETAINER Matter Activation v1.0
- Breaking change → new version. Never rename frozen fields in-place.
- Golden fixtures in `contract_golden_fixtures` table

### Authority vocabulary (frozen 6 classes)
SYS_ADMIN, FIRM_POLICY, STAFF_AUTH, ATTY_AUTH, CLIENT_AUTH, PROHIBITED
STAFF_AUTH ≠ FIRM_POLICY: staff is a named person; firm policy is a standing automated rule.

### Key database connection
- Session pooler: `aws-1-us-west-1.pooler.supabase.com:6543`
- User: `postgres.jahhqcypxjkxwrfzpyxd`
- Port 5432 = ECONNRESET. Port 6543 = works.
