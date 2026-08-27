---
category: architecture
title: "One-config enrichment model for tenant provisioning"
importance: 8
tags: []
file_paths: []
created: 2026-08-12T02:03:07.946350+00:00
updated: 2026-08-12T02:03:07.946350+00:00
memory_id: 65830129-ad50-4b1e-bab9-615cbcac1854
---

# One-config enrichment model for tenant provisioning

PROVISION_INTAKE creates base config; PROVISION_INTAKE_TENANT_CONFIGURATION enriches the SAME config (matched by tenant_id + template_code). No competing configurations. Merge logic: {**existing_payload, **new_payload}. Idempotent: unchanged payload returns 'unchanged'. PI_CORE_INTAKE is an internal template baseline, not a competing tenant configuration. Enrichment proof: POST with PI_STANDARD_INTAKE returned status=enriched, same configuration_id.

---
**Category:** `architecture` | **Importance:** 8/10
**Files:** N/A
