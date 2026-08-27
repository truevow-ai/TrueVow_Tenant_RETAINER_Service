---
category: pattern
title: "TRACE inbound document reception built"
importance: 8
tags: []
file_paths: []
created: 2026-07-24T13:47:52.308729+00:00
updated: 2026-07-24T13:47:52.308729+00:00
memory_id: ccdf33fd-41c4-4c13-8641-d80427c62b5c
---

# TRACE inbound document reception built

Inbound email: POST /api/v1/trace/webhooks/inbound-email (app/services/inbound.py:process_inbound_email). Accepts Resend webhook format with base64 attachments. Case matching via case_id in subject line regex, barcode reference, or from address. Stores to Supabase Storage under cases/{id}/inbound-email/ with source=INBOUND_EMAIL and sha256_hash for dedup. HMAC-protected. Test verified: 2 attachments stored, unmatched email correctly rejected. Inbound fax: POST /api/v1/trace/webhooks/inbound-fax. Matches by provider fax number lookup or most recent record_request. Downloads PDF from Documo media_url. Stores under cases/{id}/inbound-fax/ with source=INBOUND_FAX.

---
**Category:** `pattern` | **Importance:** 8/10
**Files:** N/A
