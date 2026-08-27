---
category: decision
title: "Contract Corrections Applied to SETTLE"
importance: 10
tags: []
file_paths: []
created: 2026-07-31T02:55:59.526477+00:00
updated: 2026-07-31T02:55:59.526477+00:00
memory_id: 31b638c4-0b1c-4f1c-bca9-24a74680ca41
---

# Contract Corrections Applied to SETTLE

Four contract corrections applied: (1) EventEnvelope frozen at v1.0.1 with Literal type, 18 required fields, product extensions prohibited at root. (2) MatterActivationEvidenceManifest aligned to 9 canonical evidence references. (3) WebhookSigner/WebhookVerifier aligned to SaaS Admin TypeScript implementation - signing string uses colon delimiters (timestamp:method:path:body_hash), path is URL path only, env vars TRUEVOW_WEBHOOK_KEY_ID/SECRET/SECONDARY_KEYS. (4) Global vs tenant separation: TenantJurisdictionActivation model created, GLOBAL_REFERENCE_TYPES and TENANT_OWNED_TYPES constants defined.

---
**Category:** `decision` | **Importance:** 10/10
**Files:** N/A
