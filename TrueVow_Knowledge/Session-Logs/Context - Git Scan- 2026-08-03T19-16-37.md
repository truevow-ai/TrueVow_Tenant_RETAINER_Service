---
category: context
title: "Git Scan: 2026-08-03T19:16:37"
importance: 8
tags: ["git-scan", "services", "automated"]
file_paths: []
created: 2026-08-03T19:16:50.877048+00:00
updated: 2026-08-03T19:16:50.877048+00:00
memory_id: adde8531-c6e2-4e81-b853-942f6b778fcf
---

# Git Scan: 2026-08-03T19:16:37

{
  "summary": {
    "timestamp": "2026-08-03T19:16:37.011042+00:00",
    "total": 14,
    "clean": 2,
    "dirty": 10,
    "missing": 2,
    "errors": 0,
    "stale_services": 12,
    "active_services": 2,
    "status_breakdown": {
      "HEALTHY": 1,
      "ACTIVE": 0,
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
      "latest_commit": "d6b5d2d docs(finance): clarify pricing schemas \u2014 Billing is canonical source, FA records approved charges",
      "status": "DIRTY",
      "dirty_files": 83,
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
      "latest_commit": "92330b5 feat(plg): PLG-SA-01 \u2014 durable onboarding orchestration replaces fire-and-forget",
      "status": "CLEAN",
      "dirty_files": 0,
      "derived_status": "HEALTHY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.0,
        "action": "start",
        "status": "ACTIVE",
        "message": "SaaS Admin: resuming from IAM branch saasadmin/iam-supabase-auth | last: PLG-SA-01 durable onboardin"
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
      "status": "DIRTY",
      "dirty_files": 115,
      "derived_status": "DIRTY",
      "badges": [],
      "agent_activity": {
        "hours_ago": 0.0,
        "action": "start",
        "status": "ACTIVE",
        "message": "Sales Ops: Phase 3 complete (state migration + HMAC + handoff), resuming to advance Phase 4/5 pipeli"
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
        "hours_ago": 63.4,
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
        "hours_ago": 88.3,
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
        "hours_ago": 87.6,
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
        "hours_ago": 953.0,
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
        "hours_ago": 188.3,
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
      "latest_commit": "5a95bec memory(Admin): SaaS Admin: Billing Entitlements + Portal Grant Verified",
      "status": "DIRTY",
      "dirty_files": 316,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 953.0,
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
      "dirty_files": 142,
      "derived_status": "NEGLECTED",
      "badges": [
        "[NEGLECTED]"
      ],
      "agent_activity": {
        "hours_ago": 188.0,
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
        "hours_ago": 63.5,
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
