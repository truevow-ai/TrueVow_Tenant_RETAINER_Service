# EventEnvelope v1.0.1 → v1.1.0 Compatibility Matrix

**Frozen:** 2026-08-01
**Blocker:** B1 (CTO Gate 0R)

---

## Version History

| Version | Date | Changes | Breaking? |
|---|---|---|---|
| v1.0.0 | 2026-07-29 | Initial freeze — 18 fields, non-nullable tenant_id, 6 legal authority classes | — |
| v1.0.1 | 2026-07-29 | Added `additionalProperties: false` enforcement | No (additive constraint) |
| v1.1.0 | 2026-08-01 | Nullable tenant_id, 7 salesops authority classes, optional authority_domain | No (relaxation) |

---

## Field Compatibility

| Field | v1.0.1 | v1.1.0 | Consumer impact |
|---|---|---|---|
| `event_id` | string uuid | string uuid | None |
| `event_type` | string (dot-notation) | string (dot-notation) | None |
| `occurred_at` | string (ISO 8601) | string (ISO 8601) | None |
| `recorded_at` | string (ISO 8601) | string (ISO 8601) | None |
| `tenant_id` | string uuid (**required, non-null**) | string uuid **or null** | **Consumers must handle null** |
| `aggregate_type` | string (minLength 1) | string (minLength 1) | None — tv.salesops.* values now valid |
| `aggregate_id` | string uuid | string uuid | None |
| `aggregate_version` | integer (min 1) | integer (min 1) | None |
| `actor_type` | string (minLength 1) | string (minLength 1) | None |
| `actor_id` | string uuid or string | string uuid or string | None |
| `authority_domain` | **Not present** | string (enum: legal, salesops, platform) | **New field — consumers should read if present** |
| `authority_class` | enum (6 legal values) | enum (13 values: 6 legal + 7 salesops) | **New values must not break validation** |
| `authority_record_id` | string uuid or null | string uuid or null | None |
| `policy_version_id` | string uuid or null | string uuid or null | None |
| `correlation_id` | string uuid | string uuid | None |
| `causation_id` | string uuid or null | string uuid or null | None |
| `payload` | object | object | None |
| `sensitivity_class` | string (minLength 1) | string (minLength 1) | None |
| `schema_version` | string (semver) | string (semver) | v1.0 remains valid |

---

## Consumer Migration Guidance

### Backward Compatibility

All v1.0.1 events are valid v1.1.0 events. The additions are relaxations, not new requirements.

### Handling `tenant_id: null`

```typescript
// Before (v1.0.1):
const tenant = envelope.tenant_id;  // always a UUID string

// After (v1.1.0):
const tenant = envelope.tenant_id;  // string | null
if (!tenant) {
  // Pre-tenant event — no tenant scope applies
  // e.g., Sales Ops discovery event
}
```

### Handling new `authority_domain`

```typescript
// Before (v1.0.1):
// authority_class was always a legal-product class

// After (v1.1.0):
if (envelope.authority_domain === 'salesops') {
  // Use salesops authority semantics
}
```

### Handling new `authority_class` values

```typescript
// If validating authority_class:
const LEGAL_CLASSES = ['sys_admin', 'firm_policy', 'staff_authorized', 'attorney', 'client', 'prohibited'];
const SALESOPS_CLASSES = ['salesops_observe', 'salesops_recommend', 'salesops_draft', 'salesops_act_bounded', 'salesops_approve', 'salesops_administer', 'salesops_never_automate'];
const ALL_CLASSES = [...LEGAL_CLASSES, ...SALESOPS_CLASSES];
```

### If you must reject pre-tenant events

Services that only handle tenant-scoped legal-product events may add a guard:

```typescript
if (!envelope.tenant_id) {
  return { valid: false, errors: ['tenant_id is required for legal-product events'] };
}
```

---

## Cross-Language Serialization

TypeScript and Python must produce identical canonicalized JSON. Test with:

```python
# Python
envelope = build_pre_tenant_event(...)
canonical = canonicalize_for_comparison(envelope)
```

```typescript
// TypeScript
const envelope = buildPreTenantEvent(...);
const canonical = canonicalizeForComparison(envelope);
```

```text
canonical_python === canonical_typescript  // must be true
```

---

## Golden Fixtures

| Fixture | tenant_id | authority_domain | Purpose |
|---|---|---|---|
| `golden-matter-activated-v1` | non-null UUID | not set (legal implied) | Legal-product event (v1.0.1) |
| `golden-envelope-v1` | non-null UUID | not set (legal implied) | Minimal envelope (v1.0.1) |
| `golden-salesops-pre-tenant-v1` | **null** | **salesops** | Pre-tenant Sales Ops event (v1.1.0) |
