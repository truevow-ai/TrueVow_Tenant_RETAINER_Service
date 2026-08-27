# Tenant Application Service

**Directory:** `TrueVow_Tenant_Application_Service`
**Git:** ✅ 231 commits
**Owner:** Ghulam Ghaus (FSD) | **Port:** 3022

TrueVow INTAKE — Multi-Bridge AI Voice Intake Platform. Phone-first legal intake via 5 voice bridges (Gemini Live, Dograh, AssemblyAI, Pipecat, xAI) with a shared WorkflowEngine.

| Attribute | Value |
|-----------|-------|
| Stack | Python (FastAPI) |
| Deployed | Fly.io |

## Integration Boundaries (as of 2026-07-25)

### What this service DOES
- Receives `tenant.created` webhook from SaaS Admin → provisions tenant DB/schema/settings (currently TODO stub — see `app/api/webhooks/saas_admin.py:209`)
- Pushes intake leads to SaaS Admin CRM via `SaaSAdminCRMClient.sync_lead()` — **client built, not yet wired to intake workflow** (`app/services/integrations/crm/saas_admin_client.py:57`)
- Serves as the voice intake platform for all bridges
- Receives workflow configs from SaaS Admin

### What this service DOES NOT do
- **Does NOT participate in the Sales Ops → application approval → CRM contact creation flow.** That handoff is entirely between Sales Ops (:3056) and SaaS Admin (:3001). The Tenant App is not involved.
- **Does NOT create CRM contacts for newly approved law firms.** That belongs to SaaS Admin's `core_contacts` table via the `POST /webhooks/sales-ops/application-approved` route.

### Cross-Service Reality

```
Sales Ops (:3056) ──→ SaaS Admin (:3001)     ← application-approved webhook (contact created in core_contacts)
SaaS Admin (:3001) ──→ Tenant App (:3022)     ← tenant.created webhook (provisioning — TODO stub)
Tenant App (:3022) ──→ SaaS Admin (:3001)     ← sync_lead() (intake lead → CRM — client built, not wired)
```

## Known Gaps
| Gap | File | Severity |
|-----|------|----------|
| `handle_tenant_created` is a TODO stub — no tenant provisioning happens | `app/api/webhooks/saas_admin.py:219-223` | HIGH |
| `SaaSAdminCRMClient.sync_lead()` built but never called from intake workflow | `app/services/integrations/crm/saas_admin_client.py:57` | HIGH |
| All 5 approval notification methods defined but orphaned | `app/services/notifications/notification_service.py:768-3226` | HIGH |
| `handle_webhook_emit` not wired to delivery service | `app/core/event_handlers.py:88` | MEDIUM |

## Recent Activity
- See [[Session-Logs]] for session history

## Code Structure
- [[Code-Maps/truevow-tenant-application-service|Structure Map]]
