---
category: context
title: "Git Scan: 2026-08-05T18:10:47"
importance: 8
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-08-05T18:11:15.052719+00:00
updated: 2026-08-05T18:11:15.052719+00:00
memory_id: c04d10db-cff4-4017-822d-0b63446b2a33
---

# Git Scan: 2026-08-05T18:10:47

{
  "summary": {
    "timestamp": "2026-08-05T18:10:47.634154+00:00",
    "total": 14,
    "clean": 7,
    "dirty": 5,
    "missing": 2,
    "errors": 0,
    "stale_services": 14,
    "active_services": 0,
    "status_breakdown": {
      "HEALTHY": 0,
      "ACTIVE": 0,
      "STALE": 9,
      "NEGLECTED": 5,
      "BLOCKED": 0,
      "FAILING": 0,
      "INCIDENT": 0,
      "DIRTY": 0,
      "UNKNOWN": 0
    },
    "observability": "NOT_DEPLOYED",
    "otel_services": 11,
    "signoz_ui": "HTTP 000",
    "overall": "DEGRADED"
  },
  "stale_services": [
    "TrueVow_Financial_Management_Service",
    "TrueVow_SaaS_Administration_Service",
    "TrueVow_Sales_Ops_Service",
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
      "latest_commit": "7c7a839 fix(FM): remove sentry dependency \u2014 deprecated across TrueVow",
      "status": "CLEAN",
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
    "TrueVow_SaaS_Administration_Service": {
      "latest_commit": "b677f2a docs: update current state, progress logs, checkpoints \u2014 PLG-SA-01 through PLG-SA-04A CLOSED, SaaS Admin FROZEN at 8c67516",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 36.3,
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
      "latest_commit": "26cf7a9 docs: progress log and checkpoint for PLG-SO-01 through SO-02C session",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 42.7,
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
        "hours_ago": 110.3,
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
      "dirty_files": 30,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 135.2,
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
      "latest_commit": "b372b1b fix(SETTLE): remove sentry dependency \u2014 deprecated across TrueVow",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 134.5,
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
      "latest_commit": "3c0b604 fix(LEVERAGE): remove sentry dependency \u2014 deprecated across TrueVow",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 999.9,
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
      "latest_commit": "c225d86 fix(VERIFY): remove sentry dependency \u2014 deprecated across TrueVow",
      "status": "CLEAN",
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
    "TrueVow_Customer_Success_CORE_Service": {
      "latest_commit": "13693f1 feat: install agency-agent skills (backend-architect, code-reviewer, security-auditor)",
      "status": "DIRTY",
      "dirty_files": 51,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 235.2,
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
      "latest_commit": "79c8149 fix(InternalOps): remove sentry dependency \u2014 deprecated across TrueVow",
      "status": "DIRTY",
      "dirty_files": 2,
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
      "latest_commit": "d3886e1 memory(Admin): Score, segment, lifecycle are separate dimensions",
      "status": "DIRTY",
      "dirty_files": 352,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 999.9,
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
      "latest_commit": "98f86a0 docs(billing): final checkpoint \u2014 architecture, key files, remaining blockers",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 234.9,
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
        "hours_ago": 110.4,
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
