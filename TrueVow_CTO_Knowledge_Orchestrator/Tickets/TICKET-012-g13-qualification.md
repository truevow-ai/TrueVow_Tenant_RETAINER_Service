# TICKET-012 — Fresh-context G13 qualification
id: TICKET-012
title: G13 qualification run (fresh context, QA mandate bar)
repo: INTAKE
status: BLOCKED
depends_on: TICKET-010, TICKET-011
goal: GOAL-2
created: 2026-08-24
updated: 2026-08-24
---
Blocked until TICKET-010 (manual testing complete) and TICKET-011 (staging healthy).

Then execute TV-INTAKE-BENJAMIN-VNEXT-E2E-QUALIFICATION-01 / STAGING-QUALIFICATION-04
with FRESH_CONTEXT=YES per CTO-ORCHESTRATOR-QA-MANDATE.md: P1 real provider booking,
P2 real LiveKit+STT+TTS, P3 CA voice, P4 OPI voice, P5 emergency voice. No mocks may
stand in for any P-item. Report PASS/CONDITIONAL_PASS/FAIL using mandate §54 format.

Done means: qualification return filed and founder briefed on G13 verdict.

---

