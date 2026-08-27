---
category: context
title: "Git Scan: 2026-07-31T03:44:13"
importance: 8
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-07-31T03:44:31.048263+00:00
updated: 2026-07-31T03:44:31.048263+00:00
memory_id: dac054d7-07dd-47a5-bc75-07f72b0ded93
---

# Git Scan: 2026-07-31T03:44:13

{
  "summary": {
    "timestamp": "2026-07-31T03:44:13.633577+00:00",
    "total": 14,
    "clean": 5,
    "dirty": 8,
    "missing": 1,
    "errors": 0,
    "stale_services": 9,
    "active_services": 5,
    "status_breakdown": {
      "HEALTHY": 4,
      "ACTIVE": 0,
      "STALE": 2,
      "NEGLECTED": 7,
      "BLOCKED": 0,
      "FAILING": 0,
      "INCIDENT": 0,
      "DIRTY": 1,
      "UNKNOWN": 0
    },
    "observability": "NOT_DEPLOYED",
    "otel_services": 12,
    "signoz_ui": "HTTP 000",
    "overall": "DEGRADED"
  },
  "stale_services": [
    "TrueVow_Financial_Management_Service",
    "TrueVow_Sales_Ops_Service",
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
      "latest_commit": "88d4c2e security: per-service key isolation \u2014 separate keys per caller-receiver pair",
      "status": "DIRTY",
      "dirty_files": 3,
      "derived_status": "DIRTY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.0,
        "action": "done",
        "status": "DONE",
        "message": "SaaS Admin: WebhookSignature v1.0 hardened + evidence recorded | outcome: per-service key isolation,"
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
      "latest_commit": "6e5d2f7 feat(tx): REST API pipeline runner + enrichment TX prefix + attorney/cohort phases 3/5/6/7/8 complete | TX: +48 cohort firms (883 total), +744 cohort attorneys (1201 total), +1497 attorneys in attorney_leads (7083 total), +1927 firms enriched | Phase 4 DB-dependent (IPv6 required)",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "STALE",
      "badges": [],
      "agent_activity": {
        "hours_ago": 81.8,
        "action": "done",
        "status": "DONE",
        "message": "Sales Ops: Completed TX pipeline phases 3/5/6/7/8 via REST API (no direct DB) | Built tx_pipeline_re"
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
      "latest_commit": "a039afd feat(security): WebhookSignature v1.0 golden fixture tests \u2014 14/14 pass",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "HEALTHY",
      "badges": [
        "[3 PENDING]"
      ],
      "agent_activity": {
        "hours_ago": 0.0,
        "action": "done",
        "status": "DONE",
        "message": "SESSION COMPLETE: WebhookSignature v1.0 implemented, golden fixtures 14/14, per-service key isolatio"
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
      "latest_commit": "29d3edc security(contracts): per-link key isolation \u2014 NO global shared secret",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "HEALTHY",
      "badges": [
        "[1 PENDING]"
      ],
      "agent_activity": {
        "hours_ago": 0.7,
        "action": "done",
        "status": "DONE",
        "message": "Portal: RETAINER Customer Portal v1 complete | 6 workspaces with contract-types, 133/133 backend tes"
      },
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
      "latest_commit": "642f030 SETTLE: Per-service key isolation \u2014 no global shared secret",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "HEALTHY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.0,
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
        "hours_ago": 865.4,
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
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 100.7,
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
      "latest_commit": "2d66444 memory(Admin): Webhook Key Mapping",
      "status": "DIRTY",
      "dirty_files": 13,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 865.4,
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
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 100.4,
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
      "latest_commit": "3eb936c docs(trace): enforce per-link webhook keys and contract source pinning",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "HEALTHY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.0,
        "action": "done",
        "status": "DONE",
        "message": "TRACE: cross-service contract rollout complete | outcome: 68 tests pass, 17 golden fixtures, webhook"
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
