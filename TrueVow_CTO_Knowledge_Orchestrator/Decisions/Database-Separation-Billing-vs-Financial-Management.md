# Billing vs Financial Management — Database-Level Separation

> **Principle**: Billing is the single source of truth for what gets charged. FM is the single source of truth for the money that moves. One contract connects them: `billing.invoice_item.ready` → FM creates the invoice.
>
> **Rule**: No table exists in both databases. No service queries the other's DB directly. All cross-service data flows through versioned, idempotent API events.

---

## Billing Service Database (`BILLING_DATABASE_URL`)

### What Billing owns: pricing, tiers, subscriptions, usage, entitlements

These are the **read-only authority** tables — every other service asks Billing "what does this tenant pay?"

---

### 1. PRICING CATALOG — the authoritative price list

#### `pricing_plans`
```
 id                  UUID PK
 plan_key            VARCHAR(50) UNIQUE   -- "solo", "growth", "team"
 vertical            VARCHAR(20)           -- "law", "dental", "medical"
 display_name        VARCHAR(100)          -- "INTAKE", "PIPELINE", "OPERATIONS"
 status              VARCHAR(20)           -- active, deprecated, hidden
 public              BOOLEAN
 available_for_new   BOOLEAN
 requires_approval   BOOLEAN
 price_monthly       DECIMAL(10,2)
 price_yearly        DECIMAL(10,2)
 attorneys_min       INTEGER
 attorneys_max       INTEGER
 routed_calls_incl   INTEGER
 voice_mins_incl     INTEGER
 call_overflow_cents INTEGER
 features            JSONB                 -- list of feature flags
 created_at          TIMESTAMPTZ
 updated_at          TIMESTAMPTZ
```

#### `pricing_addons`
```
 id                  UUID PK
 addon_key           VARCHAR(50) UNIQUE   -- "nurture_agent", "crm_export"
 vertical            VARCHAR(20)
 status              VARCHAR(20)           -- active, private_addon, deprecated
 eligible_plans      VARCHAR(50)[]         -- ["growth", "team"]
 price_monthly_cents INTEGER
 tiers               JSONB                 -- multi-tier addon config
 created_at          TIMESTAMPTZ
 updated_at          TIMESTAMPTZ
```

#### `pricing_tax_rates`
```
 id                  UUID PK
 country             VARCHAR(2)
 state               VARCHAR(2) NULLABLE
 rate                DECIMAL(5,4)
 effective_from      DATE
```

#### `pricing_products`
```
 id                  UUID PK
 product_key         VARCHAR(50) UNIQUE   -- "intake", "trace", "settle", "command"
 display_name        VARCHAR(100)
 type                VARCHAR(20)           -- plan, usage, legacy
 status              VARCHAR(20)
 public              BOOLEAN
 descriptor          VARCHAR(200)
 created_at          TIMESTAMPTZ
```

---

### 2. SUBSCRIPTIONS — which tenant is on which plan

#### `tenant_subscriptions`
```
 id                  UUID PK
 tenant_id           UUID NOT NULL INDEXED  -- Clerk org_id → SaaS Admin tenant
 plan_id             UUID FK → pricing_plans.id
 status              VARCHAR(20)            -- pending, trial, active, past_due, grace, suspended, cancelled, expired
 current_period_start TIMESTAMPTZ
 current_period_end   TIMESTAMPTZ
 trial_start          TIMESTAMPTZ NULLABLE
 trial_end            TIMESTAMPTZ NULLABLE
 cancelled_at         TIMESTAMPTZ NULLABLE
 cancel_at_period_end BOOLEAN DEFAULT FALSE
 auto_renew           BOOLEAN DEFAULT TRUE
 subscription_version INTEGER DEFAULT 1
 created_at           TIMESTAMPTZ
 updated_at           TIMESTAMPTZ
```

#### `tenant_addons`
```
 id                  UUID PK
 tenant_id           UUID NOT NULL INDEXED
 subscription_id     UUID FK → tenant_subscriptions.id
 addon_id            UUID FK → pricing_addons.id
 status              VARCHAR(20)            -- active, cancelled
 purchased_at        TIMESTAMPTZ
 expires_at          TIMESTAMPTZ
 created_at          TIMESTAMPTZ
```

#### `tenant_billing_periods`
```
 tenant_id           UUID PK (composite)
 period_start        DATE PK (composite)
 period_end          DATE
 routed_calls_used   INTEGER DEFAULT 0
 routed_calls_incl   INTEGER DEFAULT 0
 call_overflow_cents INTEGER DEFAULT 0
 voice_mins_used     INTEGER DEFAULT 0
 voice_mins_incl     INTEGER DEFAULT 0
 created_at          TIMESTAMPTZ
```

---

### 3. USAGE METERS — what got consumed

#### `usage_records`
```
 id                  UUID PK
 tenant_id           UUID NOT NULL INDEXED
 subscription_id     UUID FK → tenant_subscriptions.id
 meter_code          VARCHAR(50) INDEXED    -- "intake_billable_call", "trace_activated_matter", "settle_finalized_report"
 quantity            INTEGER DEFAULT 1
 unit                VARCHAR(20)            -- call, matter, report
 period_start        TIMESTAMPTZ
 period_end          TIMESTAMPTZ
 source_event_id     VARCHAR(255)           -- idempotency key from source event
 source_service      VARCHAR(50)            -- which service emitted the event
 ingress_idempotency VARCHAR(255) UNIQUE
 is_billed           BOOLEAN DEFAULT FALSE  -- FM has picked this up
 billed_at           TIMESTAMPTZ NULLABLE
 invoice_item_id     UUID NULLABLE          -- cross-ref to FM's invoice line item
 meta_data           JSONB
 created_at          TIMESTAMPTZ
```

#### `usage_meter_definitions`
```
 id                  UUID PK
 meter_code          VARCHAR(50) UNIQUE
 product             VARCHAR(50)
 unit                VARCHAR(20)
 customer_billable   BOOLEAN                -- internal shadow meters = false
 description         TEXT
 qualification_rules JSONB                  -- e.g. "not a test session", "not duplicate"
 source_event        VARCHAR(100)           -- e.g. "intake.call.completed"
 required_fields     JSONB
```

#### `usage_allowances`
```
 id                  UUID PK
 plan_id             UUID FK → pricing_plans.id
 meter_code          VARCHAR(50)
 included_quantity   INTEGER
 overage_cents       INTEGER
 overage_allowed     BOOLEAN DEFAULT TRUE
 hard_cap_enabled    BOOLEAN DEFAULT FALSE
```

---

### 4. ENTITLEMENTS — what features each plan unlocks

#### `entitlement_definitions`
```
 id                  UUID PK
 entitlement_code    VARCHAR(50) UNIQUE     -- "INTAKE_WEBSITE_WIDGET", "TRACE_ENGAGEMENT", "SETTLE_REPORT_GENERATE"
 product             VARCHAR(50)
 description         VARCHAR(200)
```

#### `plan_entitlements`
```
 id                  UUID PK
 plan_id             UUID FK → pricing_plans.id
 entitlement_code    VARCHAR(50) FK → entitlement_definitions.entitlement_code
 tier                VARCHAR(30) NULLABLE   -- trace_start / trace_essential / trace_complete
 UNIQUE(plan_id, entitlement_code)
```

#### `product_tiers` (TRACE, SETTLE tier configs)
```
 id                  UUID PK
 product_key         VARCHAR(50)            -- "trace", "settle"
 tier_key            VARCHAR(30)            -- "start", "essential", "complete" / "per_case", "pro"
 display_name        VARCHAR(100)
 price_cents         INTEGER
 included_quantity   INTEGER NULLABLE       -- e.g. SETTLE Pro = 15 reports
 min_commit_months   INTEGER NULLABLE
 eligible_plan_keys  VARCHAR(50)[]          -- e.g. ["growth", "team"]
```

---

### 5. UPGRADE / DOWNGRADE RULES

#### `plan_transition_rules`
```
 id                  UUID PK
 from_plan_id        UUID FK → pricing_plans.id
 to_plan_id          UUID FK → pricing_plans.id
 immediate_effect    BOOLEAN
 prorate             BOOLEAN
 reprice_unbilled    BOOLEAN
 price_difference    INTEGER NULLABLE       -- for fixed-step upgrades (e.g. trace_start→essential = $144)
```

---

### 6. INVOICE-READY LINE ITEMS — the handoff to FM

#### `invoice_line_items` (billing-side)
```
 id                  UUID PK
 tenant_id           UUID NOT NULL INDEXED
 subscription_id     UUID FK → tenant_subscriptions.id
 product_code        VARCHAR(50)
 plan_code           VARCHAR(50)
 catalog_version     VARCHAR(20)
 charge_type         VARCHAR(20)            -- SUBSCRIPTION, OVERAGE, USAGE, UPGRADE_PRORATION, CREDIT, REVERSAL, ADJUSTMENT, TAX
 description         VARCHAR(500)
 quantity            INTEGER
 unit_amount_cents   INTEGER
 subtotal_cents      INTEGER
 service_period_start TIMESTAMPTZ
 service_period_end   TIMESTAMPTZ
 source_usage_ids    UUID[]                 -- trace back to usage_records
 idempotency_key     VARCHAR(255) UNIQUE
 emitted_to_fm       BOOLEAN DEFAULT FALSE  -- has billing.invoice_item.ready been fired?
 fm_invoice_id       UUID NULLABLE          -- cross-ref to FM's invoice once created
 created_at          TIMESTAMPTZ
```

**This is where Billing's job ends.** After emitting `billing.invoice_item.ready`, FM takes over.

---

### 7. EVENT OUTBOX — guaranteed delivery to FM

#### `billing_outbox`
```
 id                  UUID PK
 event_type          VARCHAR(100)           -- "billing.invoice_item.ready"
 payload             JSONB
 tenant_id           UUID
 idempotency_key     VARCHAR(255) UNIQUE
 emitted_at          TIMESTAMPTZ
 acked_at            TIMESTAMPTZ NULLABLE   -- FM confirmed receipt
 retry_count         INTEGER DEFAULT 0
 status              VARCHAR(20)            -- pending, delivered, failed
```

---

### 8. AUDIT — billing-specific

#### `billing_audit_log`
```
 id                  UUID PK
 actor_id            UUID
 tenant_id           UUID
 action              VARCHAR(50)            -- plan_changed, usage_recorded, line_item_emitted
 object_type         VARCHAR(50)
 object_id           UUID
 before              JSONB
 after               JSONB
 correlation_id      VARCHAR(100)
 created_at          TIMESTAMPTZ
```

---

### Summary: Billing DB = 8 domains, ~16 tables

| # | Domain | Tables | Authority |
|---|--------|--------|-----------|
| 1 | Pricing Catalog | `pricing_plans`, `pricing_addons`, `pricing_tax_rates`, `pricing_products` | **Read: all services. Write: Billing only.** |
| 2 | Subscriptions | `tenant_subscriptions`, `tenant_addons`, `tenant_billing_periods` | Billing manages lifecycle |
| 3 | Usage Meters | `usage_records`, `usage_meter_definitions`, `usage_allowances` | Services write usage; Billing validates |
| 4 | Entitlements | `entitlement_definitions`, `plan_entitlements`, `product_tiers` | SaaS Admin / Tenant App query for feature gates |
| 5 | Upgrade Rules | `plan_transition_rules` | Billing enforces transition pricing |
| 6 | Invoice Line Items | `invoice_line_items` | **Billing produces; FM consumes** — the handoff |
| 7 | Outbox | `billing_outbox` | Guaranteed event delivery to FM |
| 8 | Audit | `billing_audit_log` | Pricing and usage change history |

---

## Financial Management Service Database (`FM_DATABASE_URL`)

### What FM owns: everything after the line item is emitted

FM receives `billing.invoice_item.ready` events and handles the entire money-movement lifecycle.

---

### 1. GENERAL LEDGER — double-entry accounting core

#### `legal_entity`
```
 id                  UUID PK
 code                VARCHAR(50) UNIQUE
 name                VARCHAR(255)
 country             VARCHAR(10)
 functional_currency VARCHAR(3)
 is_active           BOOLEAN
 external_org_id     TEXT                    -- maps to Clerk org_id
```

#### `book`
```
 id                  UUID PK
 legal_entity_id     UUID FK → legal_entity.id
 book_type           ENUM(ACCRUAL, CASH)
 name                VARCHAR(255)
 is_active           BOOLEAN
```

#### `gl_account`
```
 id                  UUID PK
 book_id             UUID FK → book.id
 account_code        VARCHAR(50)
 account_name        VARCHAR(255)
 account_type        ENUM(ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE, AR, AP, CASH, DEFERRED_REVENUE, ...)
 parent_account_id   UUID FK → gl_account.id NULLABLE
 is_active           BOOLEAN
```

#### `gl_account_mapping`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 book_id             UUID FK
 map_key             VARCHAR(100)            -- "INTAKE_REVENUE", "SETTLE_REVENUE", "STRIPE_FEES", "TELR_FEES"
 gl_account_id       UUID FK → gl_account.id
 UNIQUE(entity_id, book_id, map_key)
```

#### `accounting_period`
```
 id                  UUID PK
 book_id             UUID FK → book.id
 period_start        DATE
 period_end          DATE
 status              ENUM(OPEN, SOFT_CLOSED, PENDING_CLOSE_APPROVAL, CLOSED, LOCKED)
 submitted_by        UUID
 approved_by         UUID
 closed_at           TIMESTAMPTZ
 UNIQUE(book_id, period_start)
```

#### `journal_entry`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 book_id             UUID FK
 period_id           UUID FK → accounting_period.id
 entry_number        VARCHAR(100) UNIQUE
 entry_date          DATE
 description         TEXT
 reference_number    VARCHAR(255)
 status              ENUM(DRAFT, POSTED, REVERSED)  -- posted = immutable
 source_service      VARCHAR(50)                     -- "billing", "treasury", "payroll"
 source_type         VARCHAR(100)
 source_id           UUID
 idempotency_key     VARCHAR(255) UNIQUE
 posted_by           UUID
 posted_at           TIMESTAMPTZ
```

#### `journal_line`
```
 id                  UUID PK
 journal_entry_id    UUID FK → journal_entry.id
 gl_account_id       UUID FK → gl_account.id
 line_number         INTEGER
 debit_tc            DECIMAL(15,2)
 credit_tc           DECIMAL(15,2)
 currency            VARCHAR(3)
 description         TEXT
 CHECK(debit_tc >= 0 AND credit_tc >= 0)
 CHECK((debit_tc > 0 AND credit_tc = 0) OR (debit_tc = 0 AND credit_tc > 0))
```

---

### 2. ACCOUNTS RECEIVABLE — invoices, payments, customers

#### `ar_customer`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 external_customer_id VARCHAR(255) UNIQUE NULLABLE   -- links to Billing's tenant_id
 customer_name       VARCHAR(255)
 customer_code       VARCHAR(100)
 source              VARCHAR(20) DEFAULT 'BILLING'    -- BILLING or MANUAL
 is_active           BOOLEAN
```

#### `ar_invoice`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 ar_customer_id      UUID FK → ar_customer.id
 billing_line_item_ids UUID[]                          -- links back to billing.invoice_line_items
 invoice_number      VARCHAR(100) UNIQUE
 invoice_date        DATE
 due_date            DATE
 total_amount        DECIMAL(15,2)
 currency            VARCHAR(3)
 status              ENUM(DRAFT, ISSUED, PAID, PARTIALLY_PAID, OVERDUE, VOIDED, REFUNDED)
 paid_amount         DECIMAL(15,2)
 outstanding_amount  DECIMAL(15,2)
 source              VARCHAR(20) DEFAULT 'BILLING'
 created_at          TIMESTAMPTZ
```

#### `ar_invoice_line`
```
 id                  UUID PK
 ar_invoice_id       UUID FK → ar_invoice.id
 billing_line_item_id UUID NULLABLE                   -- back-link to billing's line item
 line_number         INTEGER
 description         TEXT
 quantity            DECIMAL(10,2)
 unit_price          DECIMAL(15,2)
 line_amount         DECIMAL(15,2)
 tax_amount          DECIMAL(15,2)
 service_start       DATE
 service_end         DATE
 is_deferrable       BOOLEAN                          -- triggers revenue recognition schedule
```

#### `ar_payment`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 ar_customer_id      UUID FK → ar_customer.id
 payment_date        DATE
 payment_amount      DECIMAL(15,2)
 currency            VARCHAR(3)
 payment_method      VARCHAR(50)                      -- stripe, telr, bank_transfer, manual
 payment_provider_txn_id VARCHAR(255)                  -- Stripe PaymentIntent ID / TELR txn ref
 status              ENUM(PENDING, COMPLETED, FAILED, REFUNDED, PARTIALLY_REFUNDED)
 reference_number    VARCHAR(255)
 source              VARCHAR(20) DEFAULT 'BILLING'
```

#### `ar_allocation`
```
 id                  UUID PK
 ar_payment_id       UUID FK → ar_payment.id
 ar_invoice_id       UUID FK → ar_invoice.id
 allocated_amount    DECIMAL(15,2)
 currency            VARCHAR(3)
 UNIQUE(payment_id, invoice_id)
```

#### `ar_credit_note`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 ar_invoice_id       UUID FK → ar_invoice.id NULLABLE
 ar_customer_id      UUID FK → ar_customer.id
 credit_note_number  VARCHAR(100) UNIQUE
 amount              DECIMAL(15,2)
 reason              TEXT                             -- refund, dispute, goodwill, adjustment
 status              ENUM(DRAFT, ISSUED, APPLIED, VOIDED)
 applied_to_invoice  UUID FK → ar_invoice.id NULLABLE
 journal_entry_id    UUID FK → journal_entry.id NULLABLE
```

#### `revenue_schedule`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 book_id             UUID FK → book.id
 ar_invoice_line_id  UUID FK → ar_invoice_line.id
 total_amount        DECIMAL(15,2)
 service_start       DATE
 service_end         DATE
 recognition_cadence VARCHAR(20) DEFAULT 'MONTHLY'
 status              ENUM(ACTIVE, COMPLETED, CANCELLED)
```

#### `revenue_schedule_period`
```
 id                  UUID PK
 revenue_schedule_id UUID FK → revenue_schedule.id
 period_start        DATE
 period_end          DATE
 recognition_amount  DECIMAL(15,2)
 is_recognized       BOOLEAN DEFAULT FALSE
 journal_entry_id    UUID FK → journal_entry.id NULLABLE
 UNIQUE(schedule_id, period_start)
```

---

### 3. PAYMENT PROVIDER INTEGRATION — Stripe/TELR charges

#### `payment_provider_charges`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 tenant_id           UUID                                   -- links to Billing tenant
 provider            VARCHAR(20)                            -- stripe, telr
 provider_charge_id  VARCHAR(255) UNIQUE                    -- Stripe PaymentIntent / TELR txn ID
 amount_cents        INTEGER
 currency            VARCHAR(3)
 status              VARCHAR(30)                            -- pending, succeeded, failed, refunded
 failure_code        VARCHAR(100) NULLABLE
 ar_payment_id       UUID FK → ar_payment.id NULLABLE       -- links to AR payment once matched
 idempotency_key     VARCHAR(255) UNIQUE
 created_at          TIMESTAMPTZ
```

#### `payment_provider_webhooks`
```
 id                  UUID PK
 provider            VARCHAR(20)
 event_type          VARCHAR(100)                           -- charge.succeeded, charge.refunded, etc.
 event_id            VARCHAR(255) UNIQUE
 payload             JSONB
 processed           BOOLEAN DEFAULT FALSE
 ar_payment_id       UUID FK → ar_payment.id NULLABLE
 created_at          TIMESTAMPTZ
```

---

### 4. DUNNING — collections workflow

#### `dunning_campaigns`
```
 id                  UUID PK
 tenant_id           UUID
 ar_invoice_id       UUID FK → ar_invoice.id
 stage               INTEGER                                -- 1, 2, 3...
 stage_action        VARCHAR(30)                            -- email, retry_payment, suspend, cancel
 executed_at         TIMESTAMPTZ
 result              VARCHAR(20)                            -- pending, succeeded, failed
 next_stage_at       TIMESTAMPTZ NULLABLE
```

---

### 5. DISPUTES & REFUNDS

#### `dispute`
```
 id                  UUID PK
 tenant_id           UUID
 ar_invoice_id       UUID FK → ar_invoice.id NULLABLE
 billing_line_item_id UUID NULLABLE                         -- back-link to billing
 service_type        VARCHAR(30)                            -- intake, trace, settle
 service_record_id   VARCHAR(255)
 dispute_type        VARCHAR(30)                            -- no_show, quality_issue, incomplete, billing_error
 customer_notes      TEXT
 status              ENUM(pending, investigating, approved, rejected, resolved)
 resolution_action   VARCHAR(30)                            -- refund, credit, discount, void
 resolution_notes    TEXT
 resolved_by         UUID
 resolved_at         TIMESTAMPTZ
```

#### `refund_request`
```
 id                  UUID PK
 dispute_id          UUID FK → dispute.id NULLABLE
 ar_invoice_id       UUID FK → ar_invoice.id
 ar_payment_id       UUID FK → ar_payment.id
 request_number      VARCHAR(100) UNIQUE
 refund_amount       DECIMAL(15,2)
 status              ENUM(pending_approval, approved, rejected, processing, completed, cancelled)
 requested_by        UUID                                   -- CSM user
 approved_by         UUID                                   -- Finance user
 refund_txn_id       VARCHAR(255) NULLABLE                  -- Stripe refund ID
 journal_entry_id    UUID FK → journal_entry.id NULLABLE
```

---

### 6. ACCOUNTS PAYABLE — vendor bills

#### `ap_vendor`, `ap_bill`, `ap_bill_line`, `ap_payment`, `ap_allocation`, `ap_withholding_profile`
(As currently implemented in FM — vendor invoices, approvals, payments. No change needed.)

---

### 7. TREASURY — bank accounts, settlements, reconciliation

#### `treasury_bank_account`, `treasury_bank_transaction`, `treasury_settlement`, `treasury_fx_conversion`, `treasury_transfer`
(As currently implemented in FM — bank account management, statement imports, Stripe/TELR settlement reconciliation. No change needed.)

#### `bank_reconciliation_session`, `bank_reconciliation_match`
(As currently implemented in FM — matching bank transactions to journal entries. No change needed.)

---

### 8. PAYROLL — employees, pay runs, commissions

#### `pay_group`, `hr_employee`, `pay_component_definition`, `payroll_run`, `commission_plan`, `bonus_plan`, etc.
(As currently implemented in FM — full HR/payroll module. No change needed.)

---

### 9. INTERCOMPANY — cross-entity transfers, royalties

#### `intercompany_transfer`, `royalty_agreement`, `royalty_calculation`, `intercompany_balance`
(As currently implemented in FM — cross-entity settlement. No change needed.)

---

### 10. FINANCIAL REPORTING

#### `trial_balance`, `profit_loss`, `balance_sheet`, `cash_position`, `ar_aging`, `ap_aging`
(Generated views/materialized from GL, AR, AP, Treasury. No change needed.)

---

### 11. INFRASTRUCTURE

#### `audit_log`, `idempotency_keys`, `row_audit_log`, `auth_audit_log`, `approval_policy`
(Already in FM — no change needed.)

---

### 12. BILLING SYNC — cursor tracking

#### `billing_sync_cursor`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 last_line_item_id   UUID                                   -- last invoice_line_item consumed from billing
 last_event_id       VARCHAR(255)                           -- last billing.invoice_item.ready event processed
 last_sync_at        TIMESTAMPTZ
 UNIQUE(legal_entity_id)
```

#### `billing_sync_batch`
```
 id                  UUID PK
 legal_entity_id     UUID FK
 book_id             UUID FK
 batch_number        VARCHAR(100) UNIQUE
 status              ENUM(PENDING, PROCESSING, COMPLETED, FAILED)
 items_received      INTEGER                                -- number of line items pulled
 invoices_created    INTEGER
 payments_matched    INTEGER
 failures            INTEGER
 cursor_start        VARCHAR(255)
 cursor_end          VARCHAR(255)
 started_at          TIMESTAMPTZ
 completed_at        TIMESTAMPTZ
```

---

### Summary: FM DB = 12 domains, ~50 tables

| # | Domain | Authored by | Consumes from |
|---|--------|-------------|---------------|
| 1 | General Ledger | FM | — |
| 2 | Accounts Receivable | FM | **Billing** (line items → invoices) |
| 3 | Payment Providers | FM | Stripe/TELR |
| 4 | Dunning | FM | AR invoice status |
| 5 | Disputes & Refunds | FM | CSM workflows |
| 6 | Accounts Payable | FM | Vendor bills |
| 7 | Treasury | FM | Bank feeds, Stripe/TELR settlements |
| 8 | Payroll | FM | HR data |
| 9 | Intercompany | FM | Cross-entity transfers |
| 10 | Reporting | FM | GL + AR + AP + Treasury |
| 11 | Infrastructure | FM | — |
| 12 | Billing Sync | FM | **Billing** (cursor-based consumption) |

---

## Cross-Database References (Foreign Keys Across Services)

These are NOT database foreign keys — they are **application-level cross-references** resolved via API:

| Billing Table.column | → | FM Table.column | Purpose |
|---|---|---|---|
| `usage_records.invoice_item_id` | → | `ar_invoice_line.billing_line_item_id` | Trace usage → invoice |
| `invoice_line_items.id` | → | `ar_invoice.billing_line_item_ids[]` | Billing's line item → FM's invoice |
| `invoice_line_items.id` | → | `ar_invoice_line.billing_line_item_id` | Individual line mapping |
| `invoice_line_items.id` | → | `dispute.billing_line_item_id` | Dispute traces to billing line |
| `invoice_line_items.fm_invoice_id` | → | `ar_invoice.id` | Billing knows which FM invoice |
| `tenant_subscriptions.tenant_id` | → | `ar_customer.external_customer_id` | Tenant identity |
| `billing_outbox.idempotency_key` | → | `billing_sync_cursor.last_event_id` | Sync progress |

**No database-level foreign keys cross the boundary.** Each service stores the other's UUID as an opaque reference.

---

## What Moves Where (the Unwind Plan)

### Currently in Billing ➜ Should be in FM

| What | Where it is today | Where it should be |
|------|-------------------|-------------------|
| `billing_invoices` + `billing_usage_invoice_items` | Billing DB | **FM DB** → becomes `ar_invoice` + `ar_invoice_line` |
| `billing_payments` | Billing DB | **FM DB** → becomes `ar_payment` + `payment_provider_charges` |
| `billing_disputes` | Billing DB | **FM DB** → becomes `dispute` |
| `billing_refund_requests` | Billing DB | **FM DB** → becomes `refund_request` |
| `billing_credit_ledger` | Billing DB | **FM DB** → becomes `ar_credit_note` |
| `billing_case_billing` (LEVERAGE/SETTLE per-case) | Billing DB | **Billing DB** (it's pricing → usage → line items, fits billing) |
| `billing_prepaid_credits` / `billing_prepaid_balances` | Billing DB | **Billing DB** (it's a pricing/entitlement construct) |
| `billing_settlement_submissions` (reward tracking) | Billing DB | **Billing DB** (usage meter input) |
| Growth tier tables (`attorneys`, `routing_rules`, etc.) | Billing DB | **SaaS Admin** (this is multi-tenant firm management, not billing) |
| `billing_usage_alerts` | Billing DB | **Billing DB** (usage threshold alerts make sense here) |
| `billing_dunning_*` (dunning stages) | Billing DB | **FM DB** → becomes `dunning_campaigns` |

### Already correctly in FM (no change)

| What | Status |
|------|--------|
| AR: `ar_customer`, `ar_invoice`, `ar_payment`, `ar_allocation`, `revenue_schedule` | Already in FM, but currently syncs via separate API, not the billing event contract |
| AP: `ap_vendor`, `ap_bill`, `ap_payment` | Correctly in FM |
| Treasury: all treasury tables | Correctly in FM |
| Payroll: all payroll tables | Correctly in FM |
| GL: `journal_entry`, `journal_line`, `gl_account`, etc. | Correctly in FM |
| Intercompany: all IC tables | Correctly in FM |

---

## The Event Contract (How They Connect)

```
┌─────────────────────────────────────┐     ┌──────────────────────────────────────┐
│           BILLING DB                │     │              FM DB                   │
│                                     │     │                                      │
│  usage_records                      │     │  ar_invoice                          │
│       │                             │     │       ↑                              │
│       ▼                             │     │       │ billing_line_item_ids[]      │
│  invoice_line_items                 │     │       │                              │
│       │                             │     │  ar_invoice_line                     │
│       │ billing.invoice_item.ready  │     │       ↑                              │
│       └─────────────────────────────┼─────┼───────┘ billing_line_item_id         │
│                                     │     │                                      │
│  billing_outbox                     │     │  ar_payment                          │
│       │                             │     │       │                              │
│       │ finance.invoice.paid        │     │       │ payment_provider_txn_id      │
│       ◄─────────────────────────────┼─────┼───────┘                              │
│                                     │     │                                      │
│  tenant_subscriptions               │     │  ar_customer                         │
│       │ tenant_id                   │     │       │ external_customer_id          │
│       └────────────────── ─ ─ ─ ─ ─ ┼ ─ ─ ┼ ─ ─ ─ ┘ (application-level cross-ref) │
│                                     │     │                                      │
│  billing_sync_cursor ─ ─ ─ ─ ─ ─ ─ ┼ ─ ─ ┤  billing_sync_cursor (in FM DB)     │
│  (stores last emitted event)       │     │  (stores last consumed event)         │
└─────────────────────────────────────┘     └──────────────────────────────────────┘
```

**Flow:**
1. INTAKE/TRACE/SETTLE apps emit usage events → Billing records them in `usage_records`
2. Billing runs the meter: `plan × usage × overage` = `invoice_line_items`
3. Billing emits `billing.invoice_item.ready` via `billing_outbox` (at-least-once, idempotent)
4. FM consumes the event, creates `ar_invoice` + `ar_invoice_line`, emits `finance.invoice.created`
5. FM charges the customer via Stripe/TELR, records `ar_payment`, emits `finance.invoice.paid`
6. Billing updates `invoice_line_items.emitted_to_fm = TRUE` and `usage_records.is_billed = TRUE`

---

## Security Boundaries

| Concern | Billing DB | FM DB |
|---------|-----------|-------|
| **PCI scope** | None (no card data, no payment processing) | Handles Stripe/TELR charges (tokenized, no raw PAN) |
| **Who can read** | All services (pricing catalog is public) | Internal finance team only (App1 trust domain) |
| **Who can write** | Billing service only (pricing authority) | FM service only (accounting authority) |
| **Tenant isolation** | `tenant_id` column filtering | `legal_entity_id` column filtering + Supabase RLS |
| **Immutability** | None (pricing changes are normal business ops) | Posted journal entries are immutable; corrections via reversal only |
| **Audit** | Pricing/usage change log | Full double-entry audit trail per GAAP |
