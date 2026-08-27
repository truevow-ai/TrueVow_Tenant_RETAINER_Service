# TrueVow Developer Registry
# Single source of truth for who works on what.
# Updated by the orchestrator. Read by all agents before touching any service.

## Active Developers

| Developer | Location | Services | Agent ID |
|-----------|----------|----------|----------|
| **Yasha** (Founder) | — | All — orchestrator oversight, SETTLE, LEVERAGE, VERIFY, CONNECT, Platform Analytics, Internal Ops | `yasha` |
| **Ms. Sania** | — | **Sales Ops Service** (:3056) | `sania` |
| **Ghulam Ghaus** | Faisalabad | **Tenant App Service** (:3022) + **Billing Service** (:3016) | `ghaus-fsd` |
| **Ghulam Ghous** | Islamabad | **SaaS Admin** (:3001) + **CSM CORE** (:3012) + **First Line Support** | `ghous-isb` |

## Service → Owner Mapping

| Service | Port | Owner | Backup |
|---------|------|-------|--------|
| SaaS Administration | 3001 | Ghulam Ghous (ISB) | Yasha |
| Tenant Application | 3022 | Ghulam Ghaus (FSD) | Yasha |
| Tenant Billing | 3016 | Ghulam Ghaus (FSD) | Yasha |
| Customer Success CORE | 3012 | Ghulam Ghous (ISB) | Yasha |
| First Line Support | — | Ghulam Ghous (ISB) | Yasha |
| Sales Ops | 3056 | Ms. Sania | Yasha |
| Customer Portal | 3031 | Yasha | — |
| **TRACE** | **3036** | Yasha | — |
| SETTLE | 8002 | Yasha | — |
| LEVERAGE | 3036 (shared port, hidden in portal) | Yasha | — |
| VERIFY | — | Yasha | — |
| CONNECT | — | Archived | — |
| Platform Analytics | 3071 | Yasha | — |
| Internal Ops | 3006 | Yasha | — |
| Financial Management | 3011 | Yasha | — |
| Dialogflow Intake | — | Dead | — |

## Cross-Developer Rules

1. **Read before write**: Any agent working on an owned service must first read `Session-Logs/live/` for that developer's recent activity.
2. **No silent changes**: If your change touches another developer's service boundary, write to `Session-Logs/live/cross-{date}.jsonl` before proceeding.
3. **Gate protocol applies to everyone**: ADRs, Incidents, and schema changes go through human approval regardless of who triggers them.
4. **Shared vault**: `TrueVow_Knowledge/` is the single source of truth. Every developer's agent writes session logs here. Every agent reads here before starting work.
5. **Credentials**: No developer's agent sees another developer's service credentials unless explicitly granted by the orchestrator.

## Cross-Developer Integration Boundaries (verified 2026-07-25)

### Sales Ops (Ms. Sania) → SaaS Admin (Ghulam Ghous)
- **Application approval handoff:** `POST /leads/[id]/handoff-to-saas-admin` → `POST /webhooks/sales-ops/application-approved`
- **Verified LIVE** — creates CRM contact in `core_contacts`, returns `contact_id`
- **Tenant App is NOT involved** in this flow — no Tenant App changes needed

### SaaS Admin (Ghulam Ghous) → Tenant App (Ghulam Ghaus)
- **Tenant provisioning:** `tenant.created` webhook → `POST /webhooks/saas-admin`
- **`handle_tenant_created` is a TODO stub** at `app/api/webhooks/saas_admin.py:219-223` — no provisioning occurs yet

### Tenant App (Ghulam Ghaus) → SaaS Admin (Ghulam Ghous)
- **Intake lead CRM sync:** `SaaSAdminCRMClient.sync_lead()` at `saas_admin_client.py:57` — **fully built but never called from intake workflow**
- **Subscription confirmation:** webhook ack back to SaaS Admin — operational

## Agent IDs
Used for logging, credential scoping, and state tracking. Every sub-agent must declare its agent_id in session logs.

Format: `{developer-id}-{agent-name}` (e.g. `sania-sales-agent`, `yasha-orchestrator`)
