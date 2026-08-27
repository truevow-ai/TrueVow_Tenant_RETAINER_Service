# Sales Ops Commissioning Test Matrix

**Audit date:** 2026-08-01
**Purpose:** Define the test evidence required before Sales Ops can issue a commissioning recommendation.

---

## Domain A: Sales Ops Assurance

Evidence required across the complete Sales Ops lifecycle.

### Test Group 1: Ontology Conformance

| ID | Test | Expected result | Current status |
|---|---|---|---|
| O-01 | All `pipeline_stage` values match canonical Sales Ops lifecycle | Zero unknown states | ❌ 25 implemented, 18 canonical; massive gap |
| O-02 | Unknown entity types rejected by validator | `tv.salesops.Lead` valid; `ENT-019` invalid | ❌ No validator exists |
| O-03 | Truth-status precedence enforced | `CUSTOMER_DECLARED` cannot be overwritten by `INFERRED` | ❌ No truth-status system exists |
| O-04 | Namespace boundary enforced | `tv.salesops.*` entities not writable as `tv.legal.*` | ❌ No namespace enforcement |
| O-05 | Authority class validated | `APPROVE` required for commercial approval; `DRAFT` cannot send | ❌ No authority enforcement exists |
| O-06 | Event envelope conformance | All Sales Ops events contain 18 EventEnvelope v1.0.1 fields | ❌ Zero events conform |

### Test Group 2: State Transitions

| ID | Test | Expected result | Current status |
|---|---|---|---|
| S-01 | DISCOVERED → NORMALIZED valid | Transition accepted | ❌ No DISCOVERED or NORMALIZED states |
| S-02 | DISCOVERED → APPLICATION_SUBMITTED (skip) invalid | Transition rejected | ❌ No transition validation on string-based states |
| S-03 | SUPPRESSED → IN_CAMPAIGN invalid | Transition rejected | ❌ No campaign state machine |
| S-04 | HANDED_OFF → modification invalid | Handoff package immutable after delivery | ❌ Handoff is fire-and-forget; no immutability check |
| S-05 | APPROVED_CUSTOMER → REJECTED invalid | Reversal requires explicit authority | ❌ No transition engine for downstream states |
| S-06 | Duplicate state transition idempotent | Same event replayed produces same state | ❌ No idempotency on state transitions |

### Test Group 3: Authority

| ID | Test | Expected result | Current status |
|---|---|---|---|
| A-01 | Drafting agent cannot send | `DRAFT` authority blocks `campaign_message.send` | ❌ No authority engine exists |
| A-02 | Sending agent cannot activate campaign | `ACT_BOUNDED` blocks `campaign.activate` | ❌ No authority engine exists |
| A-03 | Automated agent cannot approve customer | Automated `APPROVE` rejected; requires `HUMAN_ONLY` | ❌ No authority engine exists |
| A-04 | Sania cannot override suppression | Orchestrator blocked from un-suppressing | ❌ No policy enforcement on orchestrator |
| A-05 | Worker agent cannot erase audit | Audit deletion rejected for non-admin agents | ❌ No audit write protection |

### Test Group 4: Pipeline

| ID | Test | Expected result | Current status |
|---|---|---|---|
| P-01 | TypeScript and Python share stage definitions | Both consume same pipeline registry | ❌ Completely independent |
| P-02 | Python batch processes resumable after interrupt | Checkpoint loads and continues | ✅ Checkpoint JSON files exist |
| P-03 | Python batch processes idempotent | Same input re-processed produces same output | ❌ No idempotency key |
| P-04 | TypeScript workflow restart-safe | Failed factory stage can retry from checkpoint | ❌ No checkpointing in TS |
| P-05 | Batch lineage traceable | Every lead traceable to source artifact | ❌ Partial — batch_id exists but no full lineage |

---

## Domain B: Bridge Assurance

Evidence required across the Sales Ops → SaaS Admin boundary.

### Test Group 5: Handoff Integrity

| ID | Test | Expected result | Current status |
|---|---|---|---|
| B-01 | Handoff package schema validated | Malformed handoff rejected by SaaS Admin | ❌ No schema validation |
| B-02 | No Sales Ops entity inserted as legal entity | `CustomerCandidate` never creates `ENT-025 Matter Candidate` | ✅ No code path exists (but only by absence) |
| B-03 | No legal-client state created during qualification | Firm qualification doesn't trigger intake session | ✅ No code path exists (but only by absence) |
| B-04 | Handoff replay idempotent | Same handoff_id processed twice produces one tenant | ❌ Uses `source_lead_id` uniqueness; not `handoff_id` |
| B-05 | Organization deduplication deterministic | Same firm handed off twice resolves to same org | ❌ No dedup logic beyond source_lead_id |
| B-06 | ContactPoint verification status preserved | `TECHNICALLY_VALIDATED` contact preserved | ❌ Contact verification not mapped through |
| B-07 | Tenant receives only approved products | Products in handoff match tenant entitlements | ❌ No entitlement mapping; creates core_contact only |
| B-08 | Source provenance traceable | `customer_candidate_id` traceable through handoff to tenant | ❌ No provenance tracking beyond saas_contact_id |
| B-09 | SaaS Admin acknowledgment returns `tenant_id` | End-to-end acknowledgment received by Sales Ops | ✅ Callback `updateLeadContact()` exists |
| B-10 | SaaS Admin unavailable — Sales Ops continues | Handoff queued; no synchronous dependency | ❌ Outbox not implemented; HTTP call is synchronous |

### Test Group 6: Contract Compatibility

| ID | Test | Expected result | Current status |
|---|---|---|---|
| C-01 | Sales Ops events pass EventEnvelope v1.0.1 validation | All 18 fields present | ❌ 0/18 fields compatible |
| C-02 | WebhookSignature v1.0 enforced on all cross-service calls | HMAC-SHA256 with valid headers | ❌ Simple X-API-Key only |
| C-03 | Correlation ID survives handoff | Same correlation_id in Sales Ops event and SaaS Admin event | ❌ No correlation_id |
| C-04 | Breaking schema changes rejected | Unknown field in frozen envelope rejected | ❌ No schema enforcement |

---

## Domain C: Failure Resilience

### Test Group 7: Fault Injection

| ID | Test | Expected result | Current status |
|---|---|---|---|
| F-01 | Supabase unavailable during batch | Job fails gracefully; resumable from checkpoint | ❌ Not tested |
| F-02 | SaaS Admin unavailable during handoff | Handoff queued in outbox; retried | ❌ No outbox |
| F-03 | LLM provider timeout during enrichment | Lead marked for retry; pipeline continues | ✅ Semaphore + timeouts exist |
| F-04 | Duplicate event delivery | Second processing detected and skipped via idempotency key | ❌ No idempotency keys |
| F-05 | Circuit breaker opens on downstream service | Calls stopped; alert raised; circuit half-opens later | ✅ Circuit breakers exist (agent framework) |
| F-06 | Agent exceeds cost budget | Agent stopped; budget alert raised | ✅ Per-agent cost tracking exists |
| F-07 | Worker lock expires during batch | Lock released; next worker picks up remaining batch | ❌ No worker lock system |

---

## Summary: Commissioning Readiness

| Domain | Tests defined | Tests passable today | Pass rate |
|---|---|---|---|
| Ontology | 6 | 0 | 0% |
| State transitions | 6 | 0 | 0% |
| Authority | 5 | 0 | 0% |
| Pipeline | 5 | 1 (checkpointing) | 20% |
| Handoff bridge | 10 | 1 (B-09 acknowledgment callback) | 10% |
| Contract compatibility | 4 | 0 | 0% |
| Failure resilience | 7 | 2 (timeout + circuit breakers) | 29% |
| **Total** | **43** | **4** | **9%** |

**Commissioning recommendation:** NOT READY. 4 of 43 tests passable today (all are partial/infrastructure tests, not domain tests). Zero ontology, state-transition, authority, or contract tests pass.
