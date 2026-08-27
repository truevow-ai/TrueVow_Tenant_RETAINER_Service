---
category: architecture
title: "TrueVow Ontology v1.0 Applied to Tenant Service"
importance: 9
tags: []
file_paths: []
created: 2026-07-29T05:00:07.953222+00:00
updated: 2026-07-29T05:00:07.953222+00:00
memory_id: 752a7faa-c80b-4c50-a09b-5158fa06dc2a
---

# TrueVow Ontology v1.0 Applied to Tenant Service

The TrueVow Operations Ontology v1.0 is now the constitutional architecture for all services. Tenant intake service has been aligned:

PRODUCT DOMAINS:
- INTAKE = Acquisition (Unstructured Inquiry → Firm-Reviewable Prospect)
- RETAINER = Engagement (Firm-Approved Rep → Completed Engagement)
- TRACE = Case Production, SETTLE = Resolution, COMMAND = Operations

AUTHORITY CLASSES (every service must classify actions):
- SYS-ADMIN: automated, no case-specific approval
- FIRM-POLICY: only under approved tenant policy
- ATTY-AUTH: licensed lawyer must decide
- CLIENT-AUTH: client must authorize
- PROHIBITED: platform must never perform

AUTHORITY REGISTRY KEY (SaaS Admin owns):
- AUTH-001: Collect intake facts = SYS-ADMIN/FIRM-POLICY
- AUTH-003: Run conflict search = FIRM-POLICY (possible match only)
- AUTH-005: Approve representation = ATTY-AUTH (platform prohibited)
- AUTH-006: Select approved template = FIRM-POLICY
- AUTH-007: Modify legal terms = ATTY-AUTH (AI cannot finalize)
- AUTH-008: Explain legal effect = ATTY-AUTH (platform routes questions)
- AUTH-012: Activate matter = FIRM-POLICY + ATTY-AUTH (after gates)

NON-NEGOTIABLE INVARIANTS (all services):
- INV-001: Tenant isolation with non-null tenant_id
- INV-002: No candidate-to-client shortcut without ATTY-AUTH
- INV-004: Every active Matter has Responsible Attorney
- INV-011: No self-approval — AI can't authorize own output
- INV-017: Jurisdiction gating — no workflow without approved profile

PROSPECT LIFECYCLE (implemented in intake engine):
CONTACT_UNKNOWN → INQUIRY_RECEIVED → PROSPECTIVE_CLIENT → UNDER_FIRM_REVIEW → DECLINED|REFERRED|ENGAGEMENT_PENDING

BRIDGE INSTRUCTIONS UPDATED: All LiveKit agents now include ACT-029 authority boundary — collect facts, route questions, never decide representation.

SaaS Admin should own: ENT-005 Jurisdiction Profiles, ENT-006 Firm Policies, ENT-007 Authority Records, ENT-033 Template Definitions. Customer Portal should own: ENT-024 Consent Records, client-side signature ceremony. Billing must enforce flat/usage pricing only — no fee sharing (AUTH-011).

---
**Category:** `architecture` | **Importance:** 9/10
**Files:** N/A
