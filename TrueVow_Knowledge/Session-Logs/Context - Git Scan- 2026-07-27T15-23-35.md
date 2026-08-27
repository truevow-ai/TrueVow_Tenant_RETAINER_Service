---
category: context
title: "Git Scan: 2026-07-27T15:23:35"
importance: 8
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-07-27T15:24:28.045807+00:00
updated: 2026-07-27T15:24:28.045807+00:00
memory_id: 64f3bc66-cd06-4f8a-8785-fb6c3983d7ad
---

# Git Scan: 2026-07-27T15:23:35

{
  "summary": {
    "timestamp": "2026-07-27T15:23:35.204323+00:00",
    "total": 14,
    "clean": 0,
    "dirty": 13,
    "missing": 1,
    "errors": 0,
    "stale_services": 10,
    "active_services": 4,
    "status_breakdown": {
      "HEALTHY": 0,
      "ACTIVE": 3,
      "STALE": 1,
      "NEGLECTED": 9,
      "BLOCKED": 0,
      "FAILING": 0,
      "INCIDENT": 0,
      "DIRTY": 1,
      "UNKNOWN": 0
    },
    "observability": "DOCKER_NOT_AVAILABLE",
    "otel_services": 12,
    "signoz_ui": "HTTP 000",
    "overall": "DEGRADED"
  },
  "stale_services": [
    "TrueVow_Financial_Management_Service",
    "TrueVow_SaaS_Administration_Service",
    "TrueVow_Sales_Ops_Service",
    "Truevow_Tenant_Customer_Portal_Service",
    "TrueVow_Tenant_LEVERAGE_Service",
    "TrueVow_Tenant_VERIFY_Service",
    "TrueVow_Internal_Ops_Service",
    "TrueVow_Platform_Analytics_Service",
    "TrueVow_TWIML_SoftPhone_App",
    "TrueVow_Tenant_TRACE_Service"
  ],
  "services": {
    "TrueVow_Financial_Management_Service": {
      "latest_commit": "24be276 feat: install agency-agent skills (backend-architect, code-reviewer, security-auditor)",
      "status": "DIRTY",
      "dirty_files": 34,
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
      "latest_commit": "afd9b2d feat: install agency-agent skills (backend-architect, code-reviewer, security-auditor)",
      "status": "DIRTY",
      "dirty_files": 74,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 781.1,
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
      "latest_commit": "a96d5a4 feat: 3-tier failover for attorney_enrich.py (Playwright -> Firecrawl -> TieredFetcher). TX: 960 firms, 1136 cohort attys, enrichment via Firecrawl.",
      "status": "DIRTY",
      "dirty_files": 4,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 141.0,
        "action": "start",
        "status": "ACTIVE",
        "message": "Sales Ops: updated SANIA_DEVELOPER_GUIDE.md with full system overview (pipeline state, changes since"
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
      "latest_commit": "13f9429 fix(engine): 4 structural fixes for phantom data cascade \u2014 name split, off-topic guard, phone-like detection, pushback patterns",
      "status": "DIRTY",
      "dirty_files": 10,
      "derived_status": "ACTIVE",
      "badges": [
        "[3 PENDING]"
      ],
      "agent_activity": {
        "hours_ago": 16.4,
        "action": "start",
        "status": "ACTIVE",
        "message": "INTAKE: resuming from previous session (2026-07-18 Design Doc + LiveKit Addenda 1-16) | goal: contin"
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
      "latest_commit": "8334893 TRACE portal module: 6 pages + universal proxy + intake-to-case flow + inbound/oubound docs",
      "status": "DIRTY",
      "dirty_files": 50,
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
      "latest_commit": "c4e63f2 feat(exa): load gated Exa-enriched carriers+ages into settle_verdicts",
      "status": "DIRTY",
      "dirty_files": 4,
      "derived_status": "DIRTY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.0,
        "action": "start",
        "status": "ACTIVE",
        "message": "SETTLE: finding last session id --help"
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
        "hours_ago": 781.1,
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
      "dirty_files": 7,
      "derived_status": "ACTIVE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 16.4,
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
      "dirty_files": 2,
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
      "latest_commit": "1bd3451 memory(Admin): any | None type annotation blocks Python 3.13",
      "status": "DIRTY",
      "dirty_files": 7,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 781.1,
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
      "latest_commit": "e9b9aa7 fix: unblock .opencode/skills/ in .gitignore, remove stale node_modules",
      "status": "DIRTY",
      "dirty_files": 142,
      "derived_status": "ACTIVE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 16.1,
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
      "latest_commit": "fb452b7 fax: Twilio provider added \u2014 outbound send via pre-signed URL, inbound webhook at /twilio-inbound-fax, default FAX_PROVIDER=twilio",
      "status": "DIRTY",
      "dirty_files": 35,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 73.7,
        "action": "done",
        "status": "DONE",
        "message": "TRACE: comprehensive documentation update | outcome: 300+ line appendix added to TRACE-Agent-Coding-"
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
