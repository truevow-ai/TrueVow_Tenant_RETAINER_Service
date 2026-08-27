---
category: architecture
title: "Softphone reworked into shared multi-agent embeddable widget + Fly deploy"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T19:48:49.209391+00:00
updated: 2026-07-08T19:48:49.209391+00:00
memory_id: e2c5ff1c-61c5-411a-9f1d-0e68a29e7002
---

# Softphone reworked into shared multi-agent embeddable widget + Fly deploy

TrueVow_TWIML_SoftPhone_App evolved from standalone page to a shared softphone embedded via IFRAME in 3 Next.js dashboards (Sales Ops, Customer Success CORE, SaaS Admin) for desktop + mobile (WebRTC, no native app). Architecture: (1) auth.py - stdlib HMAC-SHA256 signed agent tokens (base64url agent_id.expiry.sig); dashboards sign with shared SOFTPHONE_SIGNING_SECRET, backend verifies before minting Twilio token. Next.js signing snippet in README mirrors it exactly. (2) Per-agent Twilio identity agent_<userid> (sanitizer strips non-alphanumerics). (3) registry.py - in-memory online-agent registry (90s TTL heartbeat via /register) + inbound resolver. (4) /voice inbound rings the SPECIFIC assigned agent (via /assign CRM seam mapping caller E.164 -> agent), fallback = ring all online, else 'unavailable'. (5) Widget: static/index.html dialpad + softphone.js vanilla JS accepting auth via ?auth= query or postMessage{type:truevow-auth}; responsive site.css. (6) CSP frame-ancestors via ALLOWED_EMBED_ORIGINS; iframe needs allow=microphone. Deploy: Dockerfile (gunicorn:8080) + fly.toml (app truevow-softphone, region iad, matches TRACE/SETTLE) - Fly gives stable HTTPS for TwiML Voice URL, NO ngrok needed. 19/19 pytest green. Verified live: signed token -> identity agent_salesrep7 + 538-char JWT, bad auth -> 401. Uses Voice SDK 2.12.3 (NOT deprecated twilio-client 1.x). Remaining manual: set TwiML App Voice URL to https://truevow-softphone.fly.dev/voice, fly secrets set (incl SOFTPHONE_SIGNING_SECRET matching dashboards), and add signAgentToken to each dashboard.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
