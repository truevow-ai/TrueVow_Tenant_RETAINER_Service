# EventEnvelope Field Decision — Machine-Verified, Frozen

**Decision date:** 2026-08-01
**Source of truth:** `contracts/event-envelope.schema.json` v1.1.0
**Verification method:** Machine-extracted regex match across all 7 committed artifacts

---

## Final Field Decision

| Field | JSON Schema | SaaS Admin TS (contracts/index.ts) | Mig 173 (golden) | Mig 176 (salesops golden) | Sales Ops TS (contracts.ts) | TS Builder | PY Builder | **Decision** |
|---|---|---|---|---|---|---|---|---|
| `schema_version` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **CANONICAL — frozen in contract** |
| `event_version` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **REMOVED — not in frozen contract** |
| `ontology_version` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **REMOVED from EventEnvelope** (correctly located in HandoffPackage.policy_version only) |

---

## Artifact Hashes (SHA-256)

| Artifact | SHA-256 (first 8) | Full SHA-256 |
|---|---|---|
| `event-envelope.schema.json` | `9EAD33A3` | `9EAD33A3853A84ACBA560D292F5CAA8FCF1A5DD1381A7AFE7961CDE6B66C4967` |
| SaaS Admin `contracts/index.ts` | `17721288` | `17721288805F81E7798AC1CEDCF7193E55EC4337AD0500AC501DA260ED1E0748` |
| Migration 173 `final_contract_fixes.sql` | `B0E6E0F8` | `B0E6E0F89CB258FFA5376A296EC72C00E5D3EAED932325008A8D7132B05426D4` |
| Migration 176 `salesops_golden_fixtures.sql` | `1EB68313` | `1EB68313F769E3F65F78933F0F1D71580D57B53A0D70A4374E74B274929CEABD` |
| Sales Ops `contracts.ts` | `B19B255E` | `B19B255EF162BA89EDF4C44595ACF91A6571D607E55D2E824E1AA83966046C6B` |
| TS `event-builder.ts` | `E1F8CFF3` | `35EFF9DF2C6BA53966C6727BBCD76F3ACDD69630953A9604A41124D71B1756F1` |
| PY `event_builder.py` | `5E73085B` | `5E73085BD9D4EF0190F2974521BF11FCE80AA6F7C67C222F5A848F533CF0E604` |

---

## What `ontology_version` is

`ontology_version` is a Sales Ops domain concept, valid only in `HandoffPackage.policy_version.ontology_version`. It records which version of `tv.salesops.*` ontology was in effect when the handoff was sealed. It is NOT an EventEnvelope field and must not appear in the envelope.

What appears in the EventEnvelope is `policy_version_id` — which references the immutable policy snapshot (including the ontology version).

---

## Rule

1. The frozen JSON Schema (`event-envelope.schema.json` SHA: `9EAD33A3`) is the sole source of truth.
2. All 7 artifacts conform to it.
3. If any artifact diverges again, the JSON Schema wins — fix the diverging artifact, not the schema.
4. This decision is frozen. Reopen only via contract versioning.
