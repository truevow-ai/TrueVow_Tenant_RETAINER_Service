---
category: context
title: "Git Scan: 2026-07-08T06:08:07"
importance: 4
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-07-08T06:08:20.459406+00:00
updated: 2026-07-08T06:08:20.459406+00:00
memory_id: a88d1f49-ae42-4724-b7cb-0bbb4435851e
---

# Git Scan: 2026-07-08T06:08:07

{
  "summary": {
    "timestamp": "2026-07-08T06:08:07.936112+00:00",
    "total": 13,
    "clean": 1,
    "dirty": 12,
    "missing": 0,
    "errors": 0,
    "stale_services": 13,
    "active_services": 0,
    "status_breakdown": {
      "HEALTHY": 0,
      "ACTIVE": 0,
      "STALE": 1,
      "NEGLECTED": 12,
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
    "TrueVow_TWIML_SoftPhone_App"
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
        "hours_ago": 315.8,
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
      "latest_commit": "7df529b fix: checkpoint sort by numeric index not string (900 > 1600 bug)",
      "status": "DIRTY",
      "dirty_files": 84,
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
    "TrueVow_Tenant_Application_Service": {
      "latest_commit": "89c8b9f test: Pipecat Cloud bridge tests (27/27) + client api_key fix",
      "status": "DIRTY",
      "dirty_files": 14,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]",
        "[3 PENDING]"
      ],
      "agent_activity": {
        "hours_ago": 315.9,
        "action": "done",
        "status": "DONE",
        "message": "Voice bridge latency optimization complete. Implemented Cartesia TTS streaming adapter with 150ms ta"
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
      "dirty_files": 9,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 27.4,
        "action": "start",
        "status": "ACTIVE",
        "message": "CTO: reviewing ecosystem state \u2014 SETTLE CL crawl running, checking all service dashboards"
      },
      "truth_loop": "failed",
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
        "hours_ago": 315.8,
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
      "latest_commit": "4d6081d feat(deploy): truth-loop gated deployment \u2014 fail blocks, GREEN deploys to fly.toml or vercel.json",
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
      "latest_commit": "4d6081d feat(deploy): truth-loop gated deployment \u2014 fail blocks, GREEN deploys to fly.toml or vercel.json",
      "status": "DIRTY",
      "dirty_files": 363,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 315.8,
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
      "latest_commit": "4d6081d feat(deploy): truth-loop gated deployment \u2014 fail blocks, GREEN deploys to fly.toml or vercel.json",
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
    }
  }
}

---
**Category:** `context` | **Importance:** 4/10
**Files:** N/A
