# TICKET-021 — Website compliance QA then lift noindex
id: TICKET-021
title: Legal/browser QA for website compliance; lift noindex when green
repo: Website
status: READY
depends_on:
goal: GOAL-3
created: 2026-08-24
updated: 2026-08-24
---
Website carries site-wide noindex,nofollow "until legal/browser QA passes" (commit
6cfb2bd, Aug 19). Run the browser QA pass (rendering, forms, mobile, console errors)
and compile the legal review checklist for the founder. Lifting noindex is a
founder verb — present findings, wait for approval, then remove the meta tag.

Done means: QA evidence filed; either noindex lifted (founder approved) or
AWAITING_FOUNDER ticket lists exactly what legal must clear.

---

