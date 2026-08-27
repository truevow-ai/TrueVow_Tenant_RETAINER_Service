---
category: context
title: "Git Scan: 2026-07-07T03:20:27"
importance: 4
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-07-07T03:20:42.910656+00:00
updated: 2026-07-07T03:20:42.910656+00:00
memory_id: 7da40235-9a4d-4dd6-9df2-b8423ff6acfe
---

# Git Scan: 2026-07-07T03:20:27

{
  "summary": {
    "timestamp": "2026-07-07T03:20:27.530069+00:00",
    "total": 13,
    "clean": 0,
    "dirty": 13,
    "missing": 0,
    "errors": 0,
    "stale_services": 12,
    "active_services": 1,
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
    "TrueVow_TWIML_SoftPhone_App"
  ],
  "services": {
    "TrueVow_Financial_Management_Service": {
      "latest_commit": "07e7966 docs: record session state + pending Supabase key-rotation reminder in WORKING_CACHE",
      "status": "DIRTY",
      "dirty_files": 33,
      "agent_activity": null
    },
    "TrueVow_SaaS_Administration_Service": {
      "latest_commit": "ee0e95f docs: record TASK 37-38 completion \u2014 SplitView + CI + security barrel",
      "status": "DIRTY",
      "dirty_files": 1,
      "agent_activity": {
        "hours_ago": 289.0,
        "action": "done",
        "status": "DONE",
        "message": "Global template infrastructure complete. LEVERAGE now inherits templates from SaaS Admin with versio"
      }
    },
    "TrueVow_Sales_Ops_Service": {
      "latest_commit": "4dbbe22 chore: agent infrastructure + shared CI template + pipeline docs",
      "status": "DIRTY",
      "dirty_files": 1,
      "agent_activity": null
    },
    "TrueVow_Tenant_Application_Service": {
      "latest_commit": "89c8b9f test: Pipecat Cloud bridge tests (27/27) + client api_key fix",
      "status": "DIRTY",
      "dirty_files": 9,
      "agent_activity": {
        "hours_ago": 289.1,
        "action": "done",
        "status": "DONE",
        "message": "Voice bridge latency optimization complete. Implemented Cartesia TTS streaming adapter with 150ms ta"
      }
    },
    "Truevow_Tenant_Customer_Portal_Service": {
      "latest_commit": "d395892 feat(settle): add trends page + fix report field mismatch + PDF proxy",
      "status": "DIRTY",
      "dirty_files": 6,
      "agent_activity": null
    },
    "TrueVow_Tenant_SETTLE-Service": {
      "latest_commit": "f97a0ec chore: ruff fixes + pdf_generator importlib check \u2014 truth-loop GREEN",
      "status": "DIRTY",
      "dirty_files": 1,
      "agent_activity": {
        "hours_ago": 0.6,
        "action": "start",
        "status": "ACTIVE",
        "message": "CTO: reviewing ecosystem state \u2014 SETTLE CL crawl running, checking all service dashboards"
      }
    },
    "TrueVow_Tenant_LEVERAGE_Service": {
      "latest_commit": "7b44160 cleanup: remove deprecated reward credit system \u2014 router, service_config, case analytics, main.py docs. Billing service remains canonical reward source.",
      "status": "DIRTY",
      "dirty_files": 1,
      "agent_activity": {
        "hours_ago": 289.0,
        "action": "blocked",
        "status": "ACTIVE",
        "message": "CA employment law validator blocked: waiting for SaaS Admin to publish v1.0 global template for CA e"
      }
    },
    "TrueVow_Tenant_VERIFY_Service": {
      "latest_commit": "4f83e0f feat(orchestrator): realtime git scan of all 13 services + startup workflow wiring",
      "status": "DIRTY",
      "dirty_files": 300,
      "agent_activity": null
    },
    "TrueVow_Customer_Success_CORE_Service": {
      "latest_commit": "b1d1bbc ops: add start_csm.bat for one-click local startup on port 3012",
      "status": "DIRTY",
      "dirty_files": 7,
      "agent_activity": null
    },
    "TrueVow_Internal_Ops_Service": {
      "latest_commit": "6348e91 all tests done 13 Feb",
      "status": "DIRTY",
      "dirty_files": 135,
      "agent_activity": null
    },
    "TrueVow_Platform_Analytics_Service": {
      "latest_commit": "4f83e0f feat(orchestrator): realtime git scan of all 13 services + startup workflow wiring",
      "status": "DIRTY",
      "dirty_files": 300,
      "agent_activity": {
        "hours_ago": 289.0,
        "action": "done",
        "status": "DONE",
        "message": "Settlement conversion dashboard built. 12 dashboards now active: metrics pipeline tracks INTAKE\u2192SETT"
      }
    },
    "TrueVow-Tenant_Billing-Service": {
      "latest_commit": "6074859 fix: gitignore source-leak in Billing Service - anchor patterns, recover ui/lib/ source, add CI workflows",
      "status": "DIRTY",
      "dirty_files": 13,
      "agent_activity": null
    },
    "TrueVow_TWIML_SoftPhone_App": {
      "latest_commit": "4f83e0f feat(orchestrator): realtime git scan of all 13 services + startup workflow wiring",
      "status": "DIRTY",
      "dirty_files": 300,
      "agent_activity": null
    }
  }
}

---
**Category:** `context` | **Importance:** 4/10
**Files:** N/A
