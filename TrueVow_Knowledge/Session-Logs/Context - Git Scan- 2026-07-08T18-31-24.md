---
category: context
title: "Git Scan: 2026-07-08T18:31:24"
importance: 4
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-07-08T18:31:40.612174+00:00
updated: 2026-07-08T18:31:40.612174+00:00
memory_id: 54319767-3283-4302-b712-276bf247eab5
---

# Git Scan: 2026-07-08T18:31:24

{
  "summary": {
    "timestamp": "2026-07-08T18:31:24.548941+00:00",
    "total": 14,
    "clean": 1,
    "dirty": 12,
    "missing": 1,
    "errors": 0,
    "stale_services": 11,
    "active_services": 3,
    "status_breakdown": {
      "HEALTHY": 0,
      "ACTIVE": 2,
      "STALE": 2,
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
    "TrueVow_SaaS_Administration_Service",
    "Truevow_Tenant_Customer_Portal_Service",
    "TrueVow_Tenant_LEVERAGE_Service",
    "TrueVow_Tenant_VERIFY_Service",
    "TrueVow_Customer_Success_CORE_Service",
    "TrueVow_Internal_Ops_Service",
    "TrueVow_Platform_Analytics_Service",
    "TrueVow-Tenant_Billing-Service",
    "TrueVow_TWIML_SoftPhone_App",
    "TrueVow_TRACE_Services"
  ],
  "services": {
    "TrueVow_Financial_Management_Service": {
      "latest_commit": "07e7966 docs: record session state + pending Supabase key-rotation reminder in WORKING_CACHE",
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
      "latest_commit": "ee0e95f docs: record TASK 37-38 completion \u2014 SplitView + CI + security barrel",
      "status": "DIRTY",
      "dirty_files": 1,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 328.2,
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
      "latest_commit": "5a25990 data: Phase 2 website crawl re-run (CA 1,880 + FL 2,100 firms)",
      "status": "DIRTY",
      "dirty_files": 4,
      "derived_status": "ACTIVE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 11.3,
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
      "latest_commit": "89c8b9f test: Pipecat Cloud bridge tests (27/27) + client api_key fix",
      "status": "DIRTY",
      "dirty_files": 17,
      "derived_status": "DIRTY",
      "badges": [
        "[3 PENDING]"
      ],
      "agent_activity": {
        "hours_ago": 0.1,
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
      "latest_commit": "d395892 feat(settle): add trends page + fix report field mismatch + PDF proxy",
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
      "latest_commit": "d50df6d docs: mandatory writeback protocol preamble \u2014 agents must report to CTO orchestrator",
      "status": "DIRTY",
      "dirty_files": 14,
      "derived_status": "ACTIVE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 10.2,
        "action": "done",
        "status": "DONE",
        "message": "SETTLE: Truth-loop fixed \u2014 ruff clean, E2E tests excluded from commit-gate (they need live server), "
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
      "latest_commit": "a97b2e7 docs: mandatory writeback protocol preamble \u2014 agents must report to CTO orchestrator",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 328.2,
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
      "latest_commit": "81af312 chore(orchestrator): TRACE Phase 1C complete \u2014 config phase + memory",
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
    "TrueVow_Customer_Success_CORE_Service": {
      "latest_commit": "b1d1bbc ops: add start_csm.bat for one-click local startup on port 3012",
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
      "latest_commit": "6348e91 all tests done 13 Feb",
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
      "latest_commit": "81af312 chore(orchestrator): TRACE Phase 1C complete \u2014 config phase + memory",
      "status": "DIRTY",
      "dirty_files": 363,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 328.2,
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
      "latest_commit": "6074859 fix: gitignore source-leak in Billing Service - anchor patterns, recover ui/lib/ source, add CI workflows",
      "status": "DIRTY",
      "dirty_files": 13,
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
      "latest_commit": "81af312 chore(orchestrator): TRACE Phase 1C complete \u2014 config phase + memory",
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
    "TrueVow_TRACE_Services": {
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
    }
  }
}

---
**Category:** `context` | **Importance:** 4/10
**Files:** N/A
