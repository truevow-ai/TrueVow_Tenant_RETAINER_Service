# RLS Policy Register — IAM-G0

| Service | Pattern | Tables Covered |
|---|---|---|
| INTAKE | `tenant_id = current_setting('app.tenant_id')::TEXT` | 14 tables (leads, contacts, intake_sessions, session_answers, bookings, alerts, audit_logs, user_roles, addresses, call_logs, edge_case_events, fraud_assessments, compliance_audit_results, session_persistence_log, booking_cancellations, crm_sync_status, rate_limit_log) |
| INTAKE (supabase) | `is_tenant_member(tenant_id)`, `has_any_role()`, `is_saas_admin()` | 20+ tables |
| SaaS Admin | `admin_all_access USING (TRUE)` + `tenant_own_data` | All admin tables |
| SaaS Admin | `tenant_roles_isolation`, `tenant_users_isolation` | RBAC tables |
| SaaS Admin | `auth.uid()::UUID` | WebSocket tables, LLM config tables |
| SaaS Admin | ENABLE + FORCE, zero policies (deny-all-anon) | Workflow tables |
| RETAINER | `tenant_id = current_setting('app.current_tenant_id')::uuid` | 5 tables (retainer workflows, representation decisions, candidate reviews, review work items, audit events) |
| Financial Management | `"tenant_isolation" USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid)` | 60+ tables |
| Communications | `auth.uid() IS NOT NULL` | conversations, conversation_recordings, conversation_chains |

## RLS Pattern Summary

- **Tenant isolation:** INTAKE, RETAINER, Financial Mgmt, SaaS Admin RBAC — `tenant_id` column check
- **Auth-based access:** SaaS Admin (websocket/LLM), Communications — `auth.uid()` check
- **Platform admin bypass:** SaaS Admin — `admin_all_access USING (TRUE)`
- **No RLS:** SETTLE, VERIFY, COMMAND, LEVERAGE, Platform Analytics, Internal Ops (backend), 2026 Website
