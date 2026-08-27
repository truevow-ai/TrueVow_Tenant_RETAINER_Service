---
source: TrueVow_Shared_Agent_Tools/agent-skills/skills/security-and-hardening/SKILL.md
imported: 2026-08-12T17:53:12.347670+00:00
skill_name: security-and-hardening
---

---
name: security-and-hardening
description: TrueVow platform security audit. Composes with /code-review for full coverage. OWASP, injection detection, secrets, authentication, threat modeling.
---

# /security-and-hardening

TrueVow-specific security review. Use **after** `/code-review` for complete coverage. `/code-review` catches general code issues; this skill adds platform-specific auth, secrets, and injection checks.

## TrueVow-Specific Checks

### 1. Secrets never in code
- No API keys, tokens, or passwords in any committed file
- `.env.example` uses placeholders only
- Check: `git diff --cached` before commit, `git log -p` for history
- **TrueVow rule:** Infisical injects secrets at runtime; no `.env.local` in CI/prod

### 2. Auth — correct domain, correct mechanism
- **Clerk 3-domain:** App1 (operators), App2 (sales LLM zone), App3 (tenants)
- **Service-to-service:** HMAC-SHA256 with `key_id + timestamp + method + path + body_hash`. Never generic `X-API-Key` for canonical contracts.
- **Cron/webhook:** Each route has **independent** auth (Bearer CRON_SECRET, provider-specific verification). Public path in middleware ≠ unauthenticated operation.
- Check: every webhook route calls `verifyTwilioSignature`, `verifyWebhook`, or equivalent provider auth

### 3. Tenant isolation — three layers
- Firm-scope query filtering
- API validation
- Supabase RLS
- PHI never in logs or URLs

### 4. Injection surface
- SQL: parameterized queries (`$1`, not string interpolation)
- No raw user input in shell commands
- LLM zone (App2): PII redacted before prompts, no direct tenant DB access, rate/response caps

### 5. Error exposure
- Production/staging UI: correlation ref only, no stack traces
- Server logs/observability: full diagnostic detail
- Use `/observability-and-instrumentation` for telemetry

## Output
- Severity-ordered findings with file:line references
- Each finding: `[CRITICAL/HIGH/MEDIUM] description → fix`
- Zero false positives preferred over missing a real issue

## Related
- `/code-review` — general code review (run first)
- `/shipping-and-launch` — fans this in automatically
- `/observability-and-instrumentation` — telemetry for security events
- TrueVow canonical decisions: `TrueVow_Context/canonical-decisions.md`
