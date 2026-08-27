---
category: architecture
title: "Security Utils Wired into SaaS Admin"
importance: 9
tags: []
file_paths: []
created: 2026-07-01T01:34:24.507873+00:00
updated: 2026-07-01T01:34:24.507873+00:00
memory_id: 11cb988a-6b0c-4a3c-a141-e73e78cae172
---

# Security Utils Wired into SaaS Admin

SaaS Admin now depends on @truevow/security-utils and @truevow/auth-client. New lib/security/index.ts module provides saasAuditLogger, logAdminAction, logSecurityEvent wrappers. Exports PII redaction, anti-exfiltration, and audit logging. Tenant App already had mature audit+PII, so no wiring needed there.

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
