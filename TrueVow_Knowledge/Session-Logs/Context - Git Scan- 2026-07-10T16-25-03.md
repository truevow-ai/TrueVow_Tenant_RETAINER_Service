---
category: context
title: "Git Scan: 2026-07-10T16:25:03"
importance: 4
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-07-10T16:25:39.696866+00:00
updated: 2026-07-10T16:25:39.696866+00:00
memory_id: bbca6a4e-3cb1-4968-adae-19d105b74c47
---

# Git Scan: 2026-07-10T16:25:03

{
  "summary": {
    "timestamp": "2026-07-10T16:25:03.674652+00:00",
    "total": 14,
    "clean": 2,
    "dirty": 12,
    "missing": 0,
    "errors": 0,
    "stale_services": 13,
    "active_services": 1,
    "status_breakdown": {
      "HEALTHY": 0,
      "ACTIVE": 0,
      "STALE": 2,
      "NEGLECTED": 11,
      "BLOCKED": 0,
      "FAILING": 0,
      "INCIDENT": 0,
      "DIRTY": 1,
      "UNKNOWN": 0
    },
    "observability": "RUNNING",
    "otel_services": 12,
    "signoz_ui": "REACHABLE",
    "overall": "DEGRADED"
  },
  "stale_services": [
    "TrueVow_Financial_Management_Service",
    "TrueVow_SaaS_Administration_Service",
    "TrueVow_Sales_Ops_Service",
    "TrueVow_Tenant_Application_Service",
    "Truevow_Tenant_Customer_Portal_Service",
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
      "latest_commit": "a1a6460 docs: add Financial Management agent coding instructions",
      "status": "DIRTY",
      "dirty_files": 33,
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
      "latest_commit": "cbec2af docs: add SaaS Admin agent coding instructions",
      "status": "DIRTY",
      "dirty_files": 2,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 374.1,
        "action": "done",
        "status": "DONE",
        "message": "Global template infrastructure complete. LEVERAGE now inherits templates from SaaS Admin with versio"
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
      "latest_commit": "bf8e244 fix: standard-list dead-end segmentation + cohort attorney tiering",
      "status": "DIRTY",
      "dirty_files": 6,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 57.2,
        "action": "start",
        "status": "ACTIVE",
        "message": "Sales Ops: upgrade Phase 3 attorney_enrich to Playwright (JS-rendered sites) + load CA firms into Su"
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
      "latest_commit": "27e8e2c docs: add INTAKE agent coding instructions",
      "status": "DIRTY",
      "dirty_files": 10,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]",
        "[3 PENDING]"
      ],
      "agent_activity": {
        "hours_ago": 46.0,
        "action": "done",
        "status": "DONE",
        "message": "Created dedicated test suite for xai_cloud voice agent bridge: tests/test_xai_cloud_bridge.py, 34/34"
      },
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 3,
        "done": 1
      }
    },
    "Truevow_Tenant_Customer_Portal_Service": {
      "latest_commit": "2b355b4 docs: add Customer Portal agent coding instructions",
      "status": "DIRTY",
      "dirty_files": 6,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]",
        "[1 PENDING]"
      ],
      "agent_activity": null,
      "truth_loop": "unknown",
      "incidents_open": 0,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 1,
        "done": 1
      }
    },
    "TrueVow_Tenant_SETTLE-Service": {
      "latest_commit": "0bf3996 feat(govdata): no-fabrication evidence gate for govdata rows",
      "status": "DIRTY",
      "dirty_files": 4,
      "derived_status": "DIRTY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.6,
        "action": "done",
        "status": "DONE",
        "message": "SETTLE: made no-fabrication the permanent process + extended gate to all pipelines | outcome: codifi"
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
      "latest_commit": "ff3cb16 docs: add LEVERAGE agent coding instructions",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 374.1,
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
        "done": 1
      }
    },
    "TrueVow_Tenant_VERIFY_Service": {
      "latest_commit": "0c23650 chore: initial commit - VERIFY blockchain certificate verification service",
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
      "latest_commit": "0ef84c9 docs: add Customer Success agent coding instructions",
      "status": "DIRTY",
      "dirty_files": 7,
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
    "TrueVow_Internal_Ops_Service": {
      "latest_commit": "1ea666d docs: add Internal Ops agent coding instructions",
      "status": "DIRTY",
      "dirty_files": 135,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]",
        "[1 PENDING]"
      ],
      "agent_activity": null,
      "truth_loop": "unknown",
      "incidents_open": 1,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 1,
        "done": 0
      }
    },
    "TrueVow_Platform_Analytics_Service": {
      "latest_commit": "c1b74e8 memory(Admin): No-fabrication is now permanent process (RULE 0) across all pipelines",
      "status": "DIRTY",
      "dirty_files": 363,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 374.1,
        "action": "done",
        "status": "DONE",
        "message": "Settlement conversion dashboard built. 12 dashboards now active: metrics pipeline tracks INTAKE\u2192SETT"
      },
      "truth_loop": "unknown",
      "incidents_open": 1,
      "tasks": {
        "active": 0,
        "blocked": 0,
        "pending": 0,
        "done": 3
      }
    },
    "TrueVow-Tenant_Billing-Service": {
      "latest_commit": "9154e9b docs: add Billing agent coding instructions",
      "status": "DIRTY",
      "dirty_files": 14,
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
    "TrueVow_TWIML_SoftPhone_App": {
      "latest_commit": "c1b74e8 memory(Admin): No-fabrication is now permanent process (RULE 0) across all pipelines",
      "status": "DIRTY",
      "dirty_files": 363,
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
    "TrueVow_Tenant_TRACE_Service": {
      "latest_commit": "b39e290 Phase 1C: Real implementations replace all stubs",
      "status": "DIRTY",
      "dirty_files": 64,
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
    }
  }
}

---
**Category:** `context` | **Importance:** 4/10
**Files:** N/A
