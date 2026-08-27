# Billing Service vs Financial Management Service — Architecture Separation

> **Audience**: Senior analysts, architecture analysts, and anyone needing to understand the boundary between TrueVow's two financial subsystems.
> **Date**: 2026-08-04
> **Status**: Current state (both services are built, Billing is production-ready, FM is code-complete with verification pending)

---

## TL;DR

| Dimension | Tenant Billing Service | Financial Management Service |
|-----------|----------------------|------------------------------|
| **Who it serves** | Customers (tenants) + platform services | TrueVow internal finance/ops team |
| **What it does** | Charges customers money | Manages TrueVow's own books |
| **Analogy** | Shopify checkout | QuickBooks / Xero back office |
| **Primary user** | Law firm (tenant) paying for INTAKE/LEVERAGE/SETTLE | TrueVow CFO, finance team, accountant |
| **Database** | Dedicated billing DB (Supabase) | Dedicated FM DB (Supabase) |
| **Scope** | Monetization of platform products | Internal accounting of the business |

---

## 1. Business Purpose

### Tenant Billing Service
The **storefront** — everything a customer sees when they pay TrueVow. It handles:
- What products cost (pricing catalog)
- How customers subscribe (tiers: Solo/Growth/Team/Founding Intelligence)
- How they pay (Stripe, TELR)
- What they're charged for (usage metering, case-based billing)
- Disputes, refunds, credits, rewards
- Feature entitlement (can this tenant access LEVERAGE validations?)

### Financial Management Service
The **back office** — TrueVow's internal accounting system. It handles:
- TrueVow's own general ledger (double-entry, multi-entity, multi-currency)
- Paying vendors and employees (AP, payroll, UAE WPS)
- Bank reconciliation and cash tracking (treasury)
- Revenue recognition (deferred revenue schedules)
- Financial reporting (P&L, Balance Sheet, Trial Balance)
- Intercompany transactions and royalty settlements

---

## 2. Service Architecture

### Tenant Billing Service

```
Port: 8000 (uvicorn) / 3016 (local dev)
Stack: Python FastAPI + Next.js 14 + Supabase PostgreSQL + Redis
Auth: Clerk JWT (tenant-facing) + X-API-Key (service-to-service) + HMAC (event ingestion)
Scheduler: APScheduler (daily billing cycle processing at 00:00 UTC)
Task Queue: ARQ (async background jobs)
Payment Gateways: Stripe + TELR (dual provider)
```

**API surface**: ~100 endpoints across 15 route groups
- `/api/v1/subscriptions` — CRUD, cancel, renew, upgrade, downgrade
- `/api/v1/invoices` — Generate, list, mark paid, download PDF
- `/api/v1/payments` — Process, retry, refund, list methods
- `/api/v1/pricing` — Calculate prices, rules, plans (public catalog)
- `/api/v1/usage` — Record, query, summarize metered usage
- `/api/v1/disputes` — Mark no-show (INTAKE), disputed (DRAFT), incomplete (SETTLE)
- `/api/v1/refunds` — CSM-initiated refunds with finance approval workflow
- `/api/v1/billing/cases` — Case-based billing for LEVERAGE ($79) and SETTLE ($399, 5 reports)
- `/api/v1/billing/credits` — Credit balance, pack purchases, pillar unlocks
- `/api/v1/billing/feature-access` — Unified entitlement check for Tenant App + Customer Portal
- `/api/v1/growth` — Multi-attorney routing, staff, branches, calendar (Growth Tier only)
- `/api/v1/analytics` — Revenue metrics (MRR, ARR, churn, CLV)
- `/api/v1/internal/events` — Ingest billing events from SaaS Admin (HMAC)
- `/api/v1/webhooks/stripe`, `/api/v1/webhooks/telr` — Payment gateway webhooks
- `/api/v1/admin` — Admin overrides, billing cycle processing, pricing tier management

**Database tables**: ~45 tables across 4 domains

| Domain | Key Tables | Purpose |
|--------|-----------|---------|
| Core Billing | `billing_subscriptions`, `pricing_subscriptions`, `billing_invoices`, `billing_payments`, `billing_usage`, `billing_usage_invoice_items`, `billing_usage_pricing_rules`, `billing_disputes`, `billing_refund_requests` | Subscription lifecycle, invoicing, payment processing, usage metering, dispute resolution |
| Platform Billing | `billing_case_billing`, `billing_credit_ledger`, `billing_pillar_unlocks`, `billing_settlement_submissions`, `billing_tenant_council_status`, `billing_leverage_reward_ledger` | Case-based billing, credit/reward system, pillar unlock progression, settlement intelligence council |
| Tier & Feature | `tiers`, `services`, `tier_features`, `addons`, `tenant_subscriptions`, `tenant_addons`, `founding_intelligence_members`, `billing_periods`, `settle_launch_config` | Pricing catalogue, feature entitlement, usage quotas, founding cohort management |
| Growth Tier | `attorneys`, `routing_rules`, `lead_assignments`, `firm_staff`, `unlock_approval_queue`, `firm_branches`, `branch_attorneys`, `attorney_calendars`, `attorney_availability`, `calendar_bookings`, `attorney_performance_metrics`, `firm_analytics_summary` | Multi-attorney firm management, lead routing, staff portal, branches, calendar integration |
| Infrastructure | `billing_audit_log`, `billing_auth_audit_log`, `billing_usage_alerts`, `billing_usage_ledger` | Audit trail, security logging, usage threshold alerts |

### Financial Management Service

```
Stack: Python FastAPI + Next.js 14 (App Router) + Supabase PostgreSQL
Auth: Supabase JWT (backend) + Clerk (frontend)
Ports: Backend on configurable port, frontend on Next.js dev server
```

**API surface**: ~130 endpoints across 6 modules

| Module | Key Endpoints | Purpose |
|--------|--------------|---------|
| General Ledger | Entities CRUD, Books, Chart of Accounts, Journal Entries (create/post/reverse/validate), Accounting Periods (generate/open/close/lock), Bank Reconciliation, Treasury Sync | Double-entry accounting core |
| Treasury | Bank Accounts, Bank Transactions (import CSV), Settlements (Stripe/TELR import), FX Conversions, Transfers | Cash management, payment gateway settlement reconciliation |
| Accounts Receivable | AR Invoices, AR Payments, AR Customers, Customer Balance, AR Aging, Billing Sync, Revenue Recognition Schedules | Customer invoicing ledger, deferred revenue |
| Accounts Payable | AP Bills, AP Vendors, AP Payments, Withholding Profiles, Bill Approval Workflow | Vendor invoice processing and payment |
| Payroll | Pay Groups, HR Employees, Pay Components, Payroll Runs (calculate/approve/post/reverse), WPS Batch Export, Commission Plans, Bonus Plans | Employee compensation, UAE WPS compliance |
| Intercompany | IC Transfers, Royalty Agreements, Royalty Calculations, IC Balance Reconciliation | Cross-entity transfers, IP royalties |
| Reporting | Trial Balance, P&L (Income Statement), Balance Sheet, Cash Position, AR/AP Aging, GL Detail | Standard financial reports |

**Database tables**: ~45 tables across 7 domains

| Domain | Key Tables | Purpose |
|--------|-----------|---------|
| General Ledger | `legal_entity`, `book` (ACCRUAL/CASH), `gl_account`, `gl_account_mapping`, `accounting_period`, `journal_entry`, `journal_line`, `journal_line_dimension`, `dimension`, `dimension_value`, `reconciliation_session`, `reconciliation_match`, `reconciliation_adjustment_batch`, `period_close_checklist`, `external_sync_cursor`, `source_object_map` | Chart of accounts, journal entries, accounting periods, bank reconciliation |
| Treasury | `treasury_bank_account`, `treasury_bank_transaction`, `treasury_settlement`, `treasury_fx_conversion`, `treasury_transfer`, `treasury_sync_cursor` | Bank accounts, statement lines, payment gateway settlements, FX, fund transfers |
| AR | `ar_customer`, `ar_invoice`, `ar_invoice_line`, `ar_payment`, `ar_allocation`, `revenue_schedule`, `revenue_schedule_period`, `billing_sync_batch` | Customer invoices, payments, deferred revenue recognition |
| AP | `ap_vendor`, `ap_bill`, `ap_bill_line`, `ap_payment`, `ap_allocation`, `ap_withholding_profile` | Vendor bills, payments, withholding tax |
| Payroll | `pay_group`, `hr_employee`, `hr_employee_bank`, `pay_component_definition`, `pay_component_assignment`, `payroll_run`, `payroll_run_item`, `payroll_run_component_line`, `payroll_payment_batch`, `commission_plan`, `commission_rule`, `commission_ledger`, `bonus_plan`, `bonus_result` | Employee data, payroll processing, commissions, bonuses, WPS export |
| Intercompany | `intercompany_transfer`, `royalty_agreement`, `royalty_calculation`, `intercompany_balance` | Cross-entity transfers, royalty calculations, IC reconciliation |
| Infrastructure | `audit_log`, `idempotency_keys`, `row_audit_log`, `auth_audit_log`, `approval_policy` | Audit trail, write idempotency, approval policy configuration |

---

## 3. Integration Points — How They Talk to Each Other

```
┌─────────────────────────────────┐      ┌──────────────────────────────────┐
│     TENANT BILLING SERVICE      │      │   FINANCIAL MANAGEMENT SERVICE   │
│         (Storefront)            │      │         (Back Office)            │
├─────────────────────────────────┤      ├──────────────────────────────────┤
│                                 │      │                                  │
│  Subscription Management        │      │  ┌──────────────────────────┐   │
│  Pricing Catalog                │      │  │  ACCOUNTS RECEIVABLE     │   │
│  Payment Processing ────────────┼──────┼──→  Sync customers/invoices │   │
│  Usage Metering                 │  AR  │  │  Revenue Recognition     │   │
│  Disputes / Refunds             │ Sync │  │  AR Aging Reports        │   │
│  Credits / Rewards              │      │  └──────────────────────────┘   │
│  Feature Entitlement            │      │                                  │
│                                 │      │  ┌──────────────────────────┐   │
│                                 │      │  │  TREASURY                │   │
│  Stripe / TELR Webhooks ────────┼──────┼──→  Settlement Import      │   │
│                                 │Treas │  │  Bank Reconciliation     │   │
│                                 │ Sync │  │  Cash Book Posting       │   │
│                                 │      │  └──────────────────────────┘   │
│                                 │      │                                  │
│                                 │      │  ┌──────────────────────────┐   │
│  Pricing API ──────────────────┼──────┼──→  Pricing Integration     │   │
│  Feature Access ───────────────┼──────┼──→  Feature Cost Lookup     │   │
│                                 │Pricing│  └──────────────────────────┘   │
│                                 │      │                                  │
│                                 │      │  ┌──────────────────────────┐   │
│  Payment Confirmations ────────┼──────┼──→  Payment Posted Events   │   │
│  Failure Alerts ───────────────┼──────┼──→  Error Notifications     │   │
│                                 │Events│  └──────────────────────────┘   │
│                                 │      │                                  │
│  SaaS Admin Events ────────────┼──────┼──  (via HMAC event ingestion)    │
│  (tenant.created, etc.)        │      │                                  │
│                                 │      │                                  │
└─────────────────────────────────┘      └──────────────────────────────────┘
```

### Integration Flows

| Flow | Direction | Data | Mechanism |
|------|-----------|------|-----------|
| **AR Sync** | Billing → FM | Customers, invoices, payments | `POST /integrations/billing/sync` with idempotency keys, cursor-based pagination |
| **Treasury Sync** | Billing → FM | Stripe/TELR settlement data | `POST /integrations/treasury/sync` for bank reconciliation |
| **Pricing/Feature Lookup** | FM → Billing | Feature costs, pricing, add-ons | FM queries Billing's `/pricing/tenants/{id}/feature-access` etc. |
| **Payment Events** | Billing → FM | Payment confirmations, failures | Payment service emits events consumed by FM |
| **Event Ingestion** | SaaS Admin → Billing | Tenant lifecycle events (created, updated) | `POST /api/v1/internal/events/ingest` with HMAC-SHA256 |
| **Service Registry** | Both → Internal Ops | Heartbeat, discovery | Both register with Internal Ops Service on startup |

---

## 4. Ownership Boundaries — Who Owns What

### Tenant Billing Service OWNS:
- **Pricing catalogue** — authoritative source of what products cost
- **Subscription state** — which tenant is on which tier
- **Payment processing** — all customer payment collection
- **Usage metering** — what gets counted and billed
- **Credit/reward ledger** — loyalty mechanics
- **Feature entitlement** — boolean "can this tenant do X" answers
- **Growth tier features** — multi-attorney routing, staff, branches, calendar
- **Dispute resolution** — no-show, quality, incomplete disputes

### Financial Management Service OWNS:
- **Chart of accounts** — authoritative chart for TrueVow's books
- **General ledger** — all journal entries, posted and immutable
- **Accounting periods** — month-end close, period locking
- **Treasury** — bank accounts, cash position, reconciliation
- **Accounts payable** — vendor bills, payments, 1099/WHT
- **Payroll** — employee compensation, UAE WPS, commissions
- **Revenue recognition** — ASC 606 / IFRS 15 compliance, deferred revenue schedules
- **Financial reporting** — P&L, Balance Sheet, Trial Balance (GAAP-compliant)
- **Intercompany** — cross-entity settlement, royalties, transfer pricing

### Neither Service Owns:
- **Tax calculation/filing** — neither service handles sales tax, VAT, or corporate tax filing
- **Audit representation** — both provide audit trails, but neither replaces an auditor

---

## 5. Database Separation — No Shared Tables

The two services have **completely separate databases** with no shared tables. This is by design:

- **Billing DB**: `postgresql://...pooler.supabase.com:5432/postgres` (billing schema)
- **FM DB**: `postgresql://...pooler.supabase.com:5432/postgres` (fm schema, different database)

Data that crosses the boundary does so via **API calls with idempotency keys**, never direct DB access. Both services use `source_object_map` / `external_sync_cursor` patterns for replay-safe, cursor-based synchronization.

### Critical: No circular ownership

```
Billing owns the billing_subscriptions table → FM does NOT query it directly
FM owns the journal_entry table → Billing does NOT query it directly
FM's ar_invoice has external_invoice_id → maps back to Billing's billing_invoices.id
```

---

## 6. Accounting Model — ACCRUAL and CASH Are First-Class

The FM Service uses a **two-book model** where both ACCRUAL and CASH are first-class books (not toggle hacks):

| Book | Driven By | Purpose |
|------|-----------|---------|
| **ACCRUAL** | Billing Service (AR sync) | Revenue recognized when earned, expenses when incurred. GAAP-compliant. |
| **CASH** | Treasury (bank statements) | Revenue recognized when cash received, expenses when cash paid. Tax-basis. |

The key insight: **CASH is Treasury-driven, not Billing-driven.** The FM service does not derive CASH entries from billing invoices. It derives them from actual bank transactions imported via treasury sync.

---

## 7. Pricing Architecture — Fail-Closed, Not Fail-Open

### Billing: Fail-Closed Catalogue
The Billing service's pricing catalogue is validated at **startup**. If the database catalogue is unavailable, **all commercial mutations return 503**. There is no fallback to hardcoded prices. This prevents accidental undercharging or billing discrepancies.

### FM: Pricing Is Read-Only
The FM service **reads** pricing from Billing but never writes it. The FM service can compute feature costs and check entitlements, but the authoritative pricing lives in Billing's `pricing_subscriptions` and `tiers` tables.

### Revenue Derivation Rule
> The Customer Portal must never send price/discount/overage values. Billing derives everything from the catalogue. FM derives everything from Billing's answers. This is a one-directional chain of authority.

---

## 8. Security & Compliance Boundaries

| Concern | Billing Service | FM Service |
|---------|----------------|------------|
| **Auth mode** | Clerk JWT (tenant) + X-API-Key (internal) + HMAC (events) | Supabase JWT (backend) + Clerk (frontend) |
| **Audit trail** | `billing_audit_log` (DB triggers) + `billing_auth_audit_log` (every request) | `audit_log` (app-level) + `row_audit_log` (DB triggers) + `auth_audit_log` |
| **Idempotency** | Redis-based middleware + application-level keys | PostgreSQL-based `idempotency_keys` table with race-condition-safe locking |
| **RLS** | 13 Growth Tier tables have Row-Level Security with tenant boundary enforcement | All tables have RLS policies via `app.current_tenant_id` GUC |
| **Immutable records** | Invoices are append-only after issuance | Posted journal entries are immutable; corrections via reversal only |
| **PCI scope** | Handles card data via Stripe/TELR (tokenized, no raw PAN storage) | Does not handle payment card data |
| **WPS compliance** | N/A | UAE Wage Protection System (WPS) batch export with SIF file format |
| **GAAP compliance** | N/A (revenue operations, not accounting) | Double-entry, deferred revenue recognition, period locking |

---

## 9. Development & Deployment

| Dimension | Billing Service | FM Service |
|-----------|----------------|------------|
| **Backend** | Python FastAPI + uvicorn | Python FastAPI + uvicorn |
| **Frontend** | Next.js 14 (Pages Router) + Tailwind | Next.js 14 (App Router) + Tailwind + shadcn/ui + Recharts + AG Grid |
| **Database** | Supabase PostgreSQL, session pooler | Supabase PostgreSQL, session pooler |
| **Migrations** | 8 Alembic migrations | 11 Alembic migrations (linear chain: 001 → 011) |
| **Container** | Fly.io (shared-cpu-2x, 1GB) | Docker + docker-compose (local), TBD for production |
| **Production** | Gunicorn + uvicorn workers (4) | TBD (CODE COMPLETE, verification pending) |
| **Task queue** | ARQ (async background jobs) | None (synchronous) |
| **Scheduler** | APScheduler (daily billing cycles) | None |
| **Cache** | Redis (idempotency, rate limiting) | None |
| **Tests** | 111 tests (all passing) | Test infrastructure exists, verification pending |
| **Status** | **PRODUCTION READY** | **CODE COMPLETE** (verification pending) |

---

## 10. Shared Infrastructure (Both Services Use)

| Component | Used By | Purpose |
|-----------|---------|---------|
| **Service Registry** (Internal Ops, port 3006) | Both | Dynamic service discovery + heartbeat |
| **Sentry** | Both | Error monitoring and crash reporting |
| **OpenTelemetry / SigNoz** | Both | Distributed tracing (OTLP on localhost:4317) |
| **Supabase** | Both | PostgreSQL hosting (separate databases) |
| **Clerk** | Both (frontends) | User authentication |
| **SendGrid / Resend** | Billing only | Email notification delivery |
| **Stripe** | Billing (payment collection), FM (settlement import) | Payment processing chain |
| **TELR** | Billing (payment collection), FM (settlement import) | MENA region payment processing |

---

## 11. Decision Log — Why Two Services Instead of One

1. **Separation of concerns**: Billing is customer-facing SaaS monetization; FM is internal double-entry accounting. Different users, different compliance regimes, different change velocities.

2. **PCI scope isolation**: Billing handles payment processing (via Stripe/TELR tokenization). FM never touches payment card data. Keeping them separate limits audit scope.

3. **Independent deployability**: Billing can be updated for pricing changes without touching the general ledger. FM can be updated for accounting rule changes without risking the checkout flow.

4. **Database isolation**: No shared tables. Cross-service data flows through versioned, idempotent APIs — not direct SQL queries. Each service's schema can evolve independently.

5. **GAAP compliance**: The FM service enforces double-entry invariants (every posted entry must balance, posted entries are immutable, closed periods are locked). These constraints would be inappropriate and overly restrictive in a customer-facing billing system that needs to handle refunds, disputes, and mid-cycle changes flexibly.

---

## 12. Known Gaps & Future Work

| Gap | Owner | Status |
|-----|-------|--------|
| Sales tax / VAT calculation | Neither | Not implemented in either service |
| Automated bank feed import (Plaid/Yodlee) | FM Treasury | Not implemented; CSV import only |
| Multi-currency AR/AP with automatic FX revaluation | FM | Partial; FX conversions exist but not automated |
| Budget vs. actuals reporting | FM Reporting | Not implemented |
| Audit representation exports (SOC 2 evidence pack) | Both | Not implemented |
| FM production deployment | FM | CODE COMPLETE, deployment pending |
| FM verification test suite | FM | CODE COMPLETE, verification pending |
