# Sales Ops to SaaS Admin Mapping — Anti-Corruption Boundary Definition

**Audit date:** 2026-08-01
**Status:** Definition only — do not implement.

---

## Principle

The Sales Ops HandoffPackage is an **input** to SaaS Admin tenant creation, not the tenant itself. Sales Ops terminology (`tv.salesops.*`) remains on the sending side. Shared Platform terminology (`tv.platform.*`) remains on the receiving side.

```
tv.salesops.*                     tv.platform.*
─────────────                     ─────────────
Sales Ops HandoffPackage     →    SaaS Admin Handoff Validator
                                        ↓
                                  Identity resolution + dedup
                                        ↓
                                  Shared Platform entities
                                        ↓
                                  Tenant creation workflow
```

---

## Mapping Table

### 1. Firm Identity → ENT-012 Organization

| Handoff field | Shared Platform entity | Resolution strategy |
|---|---|---|
| `handoff.firm_identity.legal_name` | `organizations.legal_name` | Exact match + fuzzy dedup on name + jurisdiction |
| `handoff.firm_identity.business_name` | `organizations.display_name` | Set if different from legal_name |
| `handoff.firm_identity.primary_jurisdiction` | `organizations.primary_jurisdiction` | ISO 3166-2 validation |
| `handoff.firm_identity.firm_size` | `organizations.metadata.firm_size` | Enum validation |
| `handoff.firm_identity.firm_website` | `organizations.website` | URI validation |
| `handoff.firm_identity.source_organization_id` | Stored as `organizations.source_ids[]` or `source_system_reference` | Foreign key reference for traceability |

**Anti-corruption rule:** Sales Ops `source_organization_id` is NOT the SaaS Admin `organization_id`. The validator resolves it.

### 2. Validated Contact Points → ENT-014 ContactPoint

| Handoff field | Shared Platform entity | Resolution strategy |
|---|---|---|
| `handoff.validated_contact_points[].contact_id` | Stored as `contact_points.source_contact_id` | Traceability only |
| `handoff.validated_contact_points[].contact_type` | `contact_points.contact_type` | Enum mapping |
| `handoff.validated_contact_points[].first_name` | `contact_points.first_name` | Direct map |
| `handoff.validated_contact_points[].last_name` | `contact_points.last_name` | Direct map |
| `handoff.validated_contact_points[].email` | `contact_points.email` | Dedup on email |
| `handoff.validated_contact_points[].phone` | `contact_points.phone` | E.164 normalization + dedup |
| `handoff.validated_contact_points[].validation_status` | `contact_points.verification_status` | Preserve truth status |
| `handoff.validated_contact_points[].validation_method` | `contact_points.verification_method` | Preserve provenance |
| `handoff.validated_contact_points[].validated_at` | `contact_points.verified_at` | Direct map |

**Anti-corruption rule:** `TECHNICALLY_VALIDATED` in Sales Ops maps to `contact_points.verification_status` in SaaS Admin, preserving the truth classification. `CUSTOMER_DECLARED` takes authority precedence.

### 3. Approved Customer → Input to ENT-001 Tenant Creation

| Handoff field | Tenant creation input | Notes |
|---|---|---|
| `handoff.customer_candidate_id` | `tenants.source_customer_candidate_id` | Traceability — NOT the tenant_id |
| `handoff.handoff_id` | `tenants.source_handoff_id` | Idempotency key — prevents duplicate tenant creation |
| `handoff.handoff_version` | `provisioning_requests.handoff_version` | Version tracking |
| `handoff.checksum` | `provisioning_requests.handoff_checksum` | Integrity verification |

### 4. Approved Products → Tenant Entitlement Configuration

| Handoff field | Entitlement configuration | Notes |
|---|---|---|
| `handoff.approved_products` | `product_entitlements.product` for each product | Create one entitlement row per approved product |
| `handoff.approved_plan` | `product_entitlements.plan` | FOUNDATION / GROWTH / ENTERPRISE |
| `handoff.expected_monthly_volume` | `product_entitlements.included_calls` | Capacity planning |
| `handoff.jurisdictions` | `product_entitlements.jurisdictions` | Multi-jurisdiction support |
| `handoff.practice_domains` | `product_entitlements.practice_domains` | Practice area scoping |
| `handoff.languages_required` | `product_entitlements.languages` | Language configuration |
| `handoff.implementation_requirements` | `onboarding_cases.requirements` | CSM review items |
| `handoff.custom_scope_required` | `onboarding_cases.custom_scope_flag` | Gate to custom configuration workflow |

### 5. Handoff ID → Idempotency and Provenance Reference

| Handoff field | SaaS Admin storage | Purpose |
|---|---|---|
| `handoff.handoff_id` | `provisioning_requests.idempotency_key` | Prevents duplicate tenant creation on replay |
| `handoff.customer_candidate_id` | `provisioning_requests.source_candidate_id` | Full traceability to Sales Ops domain |
| `handoff.source_application_id` | `provisioning_requests.source_application_id` | Full traceability to approval decision |
| `handoff.checksum` | `provisioning_requests.payload_checksum` | Tamper detection |

---

## Explicit Confirmation (Binding)

### ✅ Core Rules

1. **CustomerCandidate is not Tenant.** A candidate is an input to tenant creation. The tenant is created by SaaS Admin, not by Sales Ops.

2. **HandoffPackage is not Tenant.** The package is an event payload. It produces data that feeds tenant creation. It does not equal the tenant record.

3. **Approved products are not Tenant.** They become entitlement configuration associated with the tenant after creation. The tenant itself is the security boundary, not a list of products.

4. **Sales qualification is not legal Matter qualification.** Sales Ops `QualificationAssessment` evaluates commercial fit of a law firm as a TrueVow customer. The legal-product `QualificationAssessment` (ENT-026) evaluates whether an injured person's claim fits the law firm's practice. These are different domains, different actors, and different authority models.

### ❌ Forbidden Mappings

| Sales Ops concept | Must NOT map to | Reason |
|---|---|---|
| `CustomerCandidate` | `ENT-001 Tenant` | Candidate is input; Tenant is the created entity |
| `HandoffPackage` | `ENT-001 Tenant` | Package is the event; Tenant is the result |
| `QualificationAssessment` (Sales Ops) | `ENT-026 Qualification Assessment` (Legal) | Different domains |
| `Application` (Sales Ops) | `ENT-025 Matter Candidate` (Legal) | Law firm applying to TrueVow ≠ injured person's case |
| `Lead` (Sales Ops) | `ENT-019 Inquiry` (Legal) | TrueVow discovering firms ≠ firms receiving client inquiries |
| `ApprovalDecision` (Sales Ops) | `ENT-031 Representation Decision` (Legal) | Commercial approval ≠ attorney representation decision |

---

## Anti-Corruption Validator (Pseudocode)

```typescript
interface HandoffValidationResult {
  valid: boolean;
  resolved_organization_id?: string;
  resolved_contact_ids: string[];
  dedup_actions: string[];
  rejections: string[];
}

async function validateAndResolveHandoff(
  handoff: SalesOpsHandoffPackage
): Promise<HandoffValidationResult> {
  // 1. Integrity check
  const computedChecksum = sha256(canonicalJson(handoff));
  if (computedChecksum !== handoff.checksum) {
    return { valid: false, rejections: ['Checksum mismatch'] };
  }

  // 2. Idempotency check
  const existingRequest = await findProvisioningRequest(handoff.handoff_id);
  if (existingRequest?.status === 'COMPLETED') {
    return { valid: true, resolved_organization_id: existingRequest.organization_id };
  }

  // 3. Organization resolution
  const org = await resolveOrganization(handoff.firm_identity);

  // 4. Contact dedup
  const contacts = await Promise.all(
    handoff.validated_contact_points.map(resolveContact)
  );

  // 5. No legal-product entities created
  // (Enforced by only calling Shared Platform functions, never INTAKE/RETAINER)

  return {
    valid: true,
    resolved_organization_id: org.id,
    resolved_contact_ids: contacts.map(c => c.id),
  };
}
```
