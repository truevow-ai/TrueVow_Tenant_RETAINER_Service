---
category: architecture
title: "TWIML Softphone rebuilt from official Twilio Voice JS SDK quickstart"
importance: 8
tags: []
file_paths: []
created: 2026-07-08T19:12:05.380531+00:00
updated: 2026-07-08T19:12:05.380531+00:00
memory_id: 9bf953e6-4c34-40dc-a38b-b3acf6f6bf60
---

# TWIML Softphone rebuilt from official Twilio Voice JS SDK quickstart

Wiped all prior junk build in TrueVow_TWIML_SoftPhone_App (folder is fully gitignored via root .gitignore line 58, so not a git-tracked service). Rebuilt clean from TwilioDevEd/voice-javascript-sdk-quickstart-python. Backend app.py = Flask with only /token (mints Voice AccessToken+VoiceGrant) and /voice (TwiML Dial routing outbound number/client + inbound to registered browser client), plus / and /health. Frontend static/softphone.js rewritten in vanilla JS (dropped jQuery/Google CDN dep - a likely cause of prior failures). Uses current @twilio/voice-sdk v2.x from Twilio CDN with local twilio.min.js fallback (NOT the deprecated twilio-client.js 1.x). Env var names kept matching existing .env.local: TWILIO_ACCOUNT_SID, TWILIO_API_KEY_SID, TWILIO_API_KEY_SECRET, TWIML_APP_SID, TWILIO_PHONE_NUMBER. Preserved real creds in .env.local. 8/8 pytest passing; verified /health and /token mint valid 534-char JWT with real credentials. Remaining manual step: create/point TwiML App Voice Request URL to https://<host>/voice (use ngrok for local). Identity sanitizer strips non-alphanumerics so DEFAULT_IDENTITY=truevowagent.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
