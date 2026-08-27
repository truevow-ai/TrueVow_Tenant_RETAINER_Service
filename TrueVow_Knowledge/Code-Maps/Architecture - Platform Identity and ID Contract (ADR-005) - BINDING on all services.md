---
category: architecture
title: "Platform Identity and ID Contract (ADR-005) - BINDING on all services"
importance: 9
tags: []
file_paths: []
created: 2026-07-10T15:07:38.373980+00:00
updated: 2026-07-10T15:07:38.373980+00:00
memory_id: f96cb5d7-a8ca-43ae-a1e9-fe845bb4a048
---

# Platform Identity and ID Contract (ADR-005) - BINDING on all services

Cross-service ID audit (SaaS Admin, INTAKE, TRACE, SETTLE, Billing) found TRACE/SETTLE/Billing mint their own case_id and diverge on firm identity type instead of inheriting canonical IDs from SaaS Admin MDM. Canonical contract per ADR-005: Firm=clerk_org_id TEXT (Clerk org_*), User=clerk_user_id TEXT, Case=mdm_cases.case_id UUID (MDM is sole minter; others reference), Client=contact_id UUID (MDM contacts), CRM=crm_matter_id TEXT (SaaS Admin sync). Five binding rules: (1) only MDM mints case_id; (2) firm id is clerk_org_id TEXT never UUID-cast (Security Contract v1, migration 118); (3) contact_id travels alongside TRACE opaque client_token as the non-PHI cross-service client key; (4) mdm_events_outbox fans INTAKE->MDM->TRACE/SETTLE/Billing; (5) CRM matter_id propagates from SaaS Admin. TRACE migration (PLANNED, NOT executed): firm_id UUID -> clerk_org_id TEXT (RLS+FK+API+JWT claim reads), add mdm_case_id UUID nullable (keep local case_id as internal surrogate), add contact_id UUID nullable, and INTAKE CaseCreated outbox MUST be wired to MDM before TRACE prod. ADR-005 draft at TrueVow_Tenant_TRACE_Service/docs/00-Planning. Status: pending review; zero schema changes made.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
