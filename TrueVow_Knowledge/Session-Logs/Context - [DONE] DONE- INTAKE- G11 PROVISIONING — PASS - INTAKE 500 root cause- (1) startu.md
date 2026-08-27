---
category: context
title: "[DONE] DONE: INTAKE: G11 PROVISIONING \u2014 PASS | INTAKE 500 root cause: (1) startup_event crashed on truevow_auth I"
importance: 7
tags: ["agent-checkin", "done", "DONE", "TrueVow_Tenant_INTAKE_Service"]
file_paths: []
created: 2026-08-11T11:18:56.231699+00:00
updated: 2026-08-11T11:18:56.231699+00:00
memory_id: 07a0f842-291a-4019-9212-c931b9f5752a
---

# [DONE] DONE: INTAKE: G11 PROVISIONING — PASS | INTAKE 500 root cause: (1) startup_event crashed on truevow_auth I

{"agent_id": "TrueVow_Tenant_INTAKE_Service", "action": "done", "status": "DONE", "message": "INTAKE: G11 PROVISIONING \u2014 PASS | INTAKE 500 root cause: (1) startup_event crashed on truevow_auth ImportError, blocking ORM init; (2) session autoflush=False caused FK violation on provisioning_command insert; (3) intake_template_versions missing runtime_registry_version + effective_to columns. Fixes: uncoupled ORM import from other imports, wrapped truevow_auth in try/except, added session.flush() before FK insert, added missing columns via ALTER TABLE. | Learned: The provisioning contract was intact at POST /api/v1/internal/tenants/provision \u2014 the confusion was between the lifecycle webhook (/webhooks/saas-admin) and the canonical provisioning endpoint. The canary provisioned 2 INTAKE configs for tenant ec105c72-...: PI_STANDARD_INTAKE + PI_CORE_INTAKE, both VALIDATED. 6 commands scoped correctly: 2 DELIVERED, 4 PENDING (held). | Next: G11 activation, then G13 Benjamin readiness", "timestamp": "2026-08-11T11:18:56.231341+00:00", "working_dir": "C:\\Users\\yasha\\OneDrive\\Documents\\TrueVow\\Cursor\\TrueVow_Tenant_INTAKE_Service"}

---
**Category:** `context` | **Importance:** 7/10
**Files:** N/A
