# Canonical Endpoint Path Decision

**Decision date:** 2026-08-01
**Decision authority:** CTO-Knowledge-Orchestrator

---

## Decision

**The canonical path for the Sales Ops → SaaS Admin handoff webhook is:**

```text
POST /api/v1/webhooks/sales-ops/application-approved
```

This path is used by all 6 touchpoints and must match byte-for-byte for HMAC signing to succeed.

---

## Verified Byte-for-Byte Consistency

| Layer | Path | File | Line | Matches? |
|---|---|---|---|---|
| Sender (Sales Ops) | `/api/v1/webhooks/sales-ops/application-approved` | `lib/integrations/saas-admin/webhook-client.ts` | 40 | |
| Receiver HMAC canonical path | `/api/v1/webhooks/sales-ops/application-approved` | `app/api/v1/webhooks/sales-ops/application-approved/route.ts` | 53 | |
| Receiver URL construction | `/api/v1/webhooks/sales-ops/application-approved` | Same file | 438 | |
| Test import | `@/app/api/v1/webhooks/sales-ops/application-approved/route` | `tests/api/v1/webhooks/sales-ops/application-approved.test.ts` | 65 | |
| Test URL | `/api/v1/webhooks/sales-ops/application-approved` | Same file | 67 | |
| Alias (backward compat only) | Re-exports v1 implementation | `app/webhooks/sales-ops/application-approved/route.ts` | 10 | N/A (re-export) |

**All 5 active touchpoints use the same path string.** The alias at `/webhooks/sales-ops/application-approved` is a backward-compatibility re-export and does not participate in HMAC signing.

---

## Why v1.0 Path Was Incorrect

The earlier `CTO_GATE_0_DECISION.md` and `service-dependency-map.md` referenced:

```text
POST /webhooks/sales-ops/application-approved
```

This was based on the now-corrected alias file doc comment. The actual code has always used `/api/v1/webhooks/sales-ops/application-approved`. The HMAC signing string was never broken because the receiver hardcodes the path at line 53 rather than reading it from the URL.

No production impact — the signing path and the receiver path have always matched because both use the explicit string at line 53. Only the documentation was inconsistent.

---

## Documentation Updated

| Document | Fix |
|---|---|
| `service-dependency-map.md` | Already reads `/api/v1/webhooks/sales-ops/application-approved` (corrected in B5) |
| `CTO_GATE_0_DECISION.md` | Updated to canonical path |
| `CTO_GATE_0_DIRECTIVE.md` | Updated to canonical path |
| Alias route doc comment | Corrected |

---

## Rule

The canonical path appears in 3 binding places:

1. **Sender:** `this.webhookPath` in `webhook-client.ts` (controls URL construction)
2. **Receiver HMAC:** `const path = '/api/v1/webhooks/sales-ops/application-approved'` (controls signing string verification)
3. **Test:** `const URL = '/api/v1/webhooks/sales-ops/application-approved'` (must match exactly)

Any change to the path requires:

- Simultaneous update to all 3 binding places
- Update to the WebhookSignature contract registry entry
- Re-signing of all golden fixtures
- Re-execution of all HMAC negative tests (N3, N4, N11)
- No redirect — signed webhooks must land at the exact path they were signed for
