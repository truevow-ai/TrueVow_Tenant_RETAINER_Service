---
category: context
title: "Git Scan: 2026-08-04T05:58:47"
importance: 8
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-08-04T05:59:02.284977+00:00
updated: 2026-08-04T05:59:02.284977+00:00
memory_id: 48259084-4a9b-4da8-85ec-27d0c3cdc14b
---

# Git Scan: 2026-08-04T05:58:47

{
  "summary": {
    "timestamp": "2026-08-04T05:58:47.741940+00:00",
    "total": 14,
    "clean": 1,
    "dirty": 11,
    "missing": 2,
    "errors": 0,
    "stale_services": 12,
    "active_services": 2,
    "status_breakdown": {
      "HEALTHY": 0,
      "ACTIVE": 1,
      "STALE": 3,
      "NEGLECTED": 9,
      "BLOCKED": 0,
      "FAILING": 0,
      "INCIDENT": 0,
      "DIRTY": 1,
      "UNKNOWN": 0
    },
    "observability": "NOT_DEPLOYED",
    "otel_services": 11,
    "signoz_ui": "HTTP 000",
    "overall": "DEGRADED"
  },
  "stale_services": [
    "TrueVow_Financial_Management_Service",
    "TrueVow_Tenant_Application_Service",
    "Truevow_Tenant_Customer_Portal_Service",
    "TrueVow_Tenant_SETTLE-Service",
    "TrueVow_Tenant_LEVERAGE_Service",
    "TrueVow_Tenant_VERIFY_Service",
    "TrueVow_Customer_Success_CORE_Service",
    "TrueVow_Internal_Ops_Service",
    "TrueVow_Platform_Analytics_Service",
    "TrueVow-Tenant_Billing-Service",
    "TrueVow_TWIML_SoftPhone_App",
    "TrueVow_Tenant_TRACE_Service"
  ],
  "services": {
    "TrueVow_Financial_Management_Service": {
      "latest_commit": "3f587e5 docs(customer-finance): PLG-FM-CF-03C commissioning report + status update",
      "status": "DIRTY",
      "dirty_files": 86,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": null,
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_SaaS_Administration_Service": {
      "latest_commit": "8c67516 feat(plg): PLG-SA-01 through PLG-SA-04 \u2014 durable onboarding, commercial containment, commissioning authority, INTAKE provisioning contract",
      "status": "DIRTY",
      "dirty_files": 1,
      "derived_status": "DIRTY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.1,
        "action": "done",
        "status": "DONE",
        "message": "SaaS Admin: PLG-SA-04A RECONCILED \u2014 v27 attribution error resolved (actual commit 8c67516, not 92330"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Sales_Ops_Service": {
      "latest_commit": "c31c233 feat(plg): PLG-SO-01 through SO-02C \u2014 segmentation, channel-neutral campaigns, regional batches, auth hardening",
      "status": "DIRTY",
      "dirty_files": 78,
      "derived_status": "ACTIVE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 6.5,
        "action": "done",
        "status": "DONE",
        "message": "Sales Ops: PLG-SO-01 through SO-02C complete. Awaiting staging agent for final commissioning. Baseli"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Tenant_Application_Service": {
      "latest_commit": "",
      "status": "MISSING",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 74.1,
        "action": "done",
        "status": "DONE",
        "message": "INTAKE: deployed 4 engine fixes for transfer re-engagement + billing architecture saved to memory | "
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "Truevow_Tenant_Customer_Portal_Service": {
      "latest_commit": "e4415ff chore: update progress log \u2014 billing architecture + pricing finalized",
      "status": "DIRTY",
      "dirty_files": 26,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 99.0,
        "action": "done",
        "status": "DONE",
        "message": "Portal: RETAINER Customer Portal v1 complete | 6 workspaces with contract-types, 133/133 backend tes"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Tenant_SETTLE-Service": {
      "latest_commit": "951d773 SETTLE: Billing usage integration \u2014 emit settle.report.finalized events",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 98.3,
        "action": "done",
        "status": "DONE",
        "message": "SETTLE: WebhookSignature v1.0 fully contract-aligned \u2014 per-service key isolation, 17 golden fixtures"
      },
      "truth_loop": "green",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Tenant_LEVERAGE_Service": {
      "latest_commit": "a523f13 feat: install agency-agent skills (backend-architect, code-reviewer, security-auditor)",
      "status": "DIRTY",
      "dirty_files": 1,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 963.7,
        "action": "blocked",
        "status": "ACTIVE",
        "message": "CA employment law validator blocked: waiting for SaaS Admin to publish v1.0 global template for CA e"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Tenant_VERIFY_Service": {
      "latest_commit": "fbe4da1 feat: install agency-agent skills (backend-architect, code-reviewer, security-auditor)",
      "status": "DIRTY",
      "dirty_files": 1,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": null,
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Customer_Success_CORE_Service": {
      "latest_commit": "13693f1 feat: install agency-agent skills (backend-architect, code-reviewer, security-auditor)",
      "status": "DIRTY",
      "dirty_files": 51,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 199.0,
        "action": "start",
        "status": "ACTIVE",
        "message": "CSM: resuming previous session | checking current state | goal: continue where we left off"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Internal_Ops_Service": {
      "latest_commit": "2720053 sanitized: remove supabase secrets from history",
      "status": "DIRTY",
      "dirty_files": 3,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": null,
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Platform_Analytics_Service": {
      "latest_commit": "fb4f635 memory(Admin): IAM permission check: requireHITLPermission() uses canonical codes, not hardcoded role lists",
      "status": "DIRTY",
      "dirty_files": 316,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 963.7,
        "action": "done",
        "status": "DONE",
        "message": "Settlement conversion dashboard built. 12 dashboards now active: metrics pipeline tracks INTAKE\u2192SETT"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow-Tenant_Billing-Service": {
      "latest_commit": "74eae73 feat(billing): full pricing architecture \u2014 usage meters, entitlements, subscription states, billing-accounting contract, COMMAND pricing, upgrade rules",
      "status": "DIRTY",
      "dirty_files": 161,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 198.7,
        "action": "done",
        "status": "DONE",
        "message": "Billing: fixed test suite \u2014 all 111 tests pass (was 55 failing) | outcome: 111 passed, 0 failed, 1 s"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_TWIML_SoftPhone_App": {
      "latest_commit": "",
      "status": "MISSING",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": null,
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    },
    "TrueVow_Tenant_TRACE_Service": {
      "latest_commit": "4d6fec4 chore: update AGENTS.md session history for Aug 1 milestone",
      "status": "DIRTY",
      "dirty_files": 12,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 74.2,
        "action": "done",
        "status": "DONE",
        "message": "TRACE: billing plan code, millisecond timestamp fix, migration 0018, /ready endpoint live | outcome:"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 0
      }
    }
  }
}

---
**Category:** `context` | **Importance:** 8/10
**Files:** N/A
