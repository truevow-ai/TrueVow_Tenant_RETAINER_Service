# TICKET-004 — Ecosystem config reconciliation
id: TICKET-004
title: Reconcile ecosystem config.yaml with repo reality
repo: SaaS Admin
status: READY
depends_on:
goal: GOAL-1
created: 2026-08-24
updated: 2026-08-24
---
TrueVow_Shared_Orchestration/config.yaml is stale against disk reality:

1. services block still lists TrueVow_Tenant_Application_Service — the repo was renamed
   TrueVow_Tenant_INTAKE_Service. Update path/keys (dispatch intents too).
2. RETAINER (TrueVow_Tenant_RETAINER_Service), COMMAND (TrueVow_Tenant_COMMAND_Service),
   and Website (2026_TrueVow_Website) are absent — register them with stack/type.
3. TRACE note claims "Auth: Clerk (platform standard) ... NO Supabase Auth migration"
   — founder overturned this on 2026-08-24: Supabase Auth is sole human IdP platform-wide.
   Fix the note to match; code-level migration is TICKET-020 scope, not here.
4. First Line Support marked replaced_by Chatwoot — keep historical marker, no action.

Done means: config.yaml paths all resolve on disk; registry matches Developer Start Here v4 §4.

---

