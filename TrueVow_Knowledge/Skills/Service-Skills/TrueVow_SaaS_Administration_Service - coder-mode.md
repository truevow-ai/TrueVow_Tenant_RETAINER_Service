---
source: TrueVow_SaaS_Administration_Service/.opencode/skills/coder-mode/SKILL.md
service: TrueVow_SaaS_Administration_Service
type: internal-mdm
stack: ["nextjs", "typescript", "postgresql", "supabase"]
imported: 2026-08-12T17:53:14.690844+00:00
skill_name: coder-mode
---
# SaaS Admin Coder Mode

## Service-specific patterns only (global patterns in truevow-build)

### Migration pattern
- SQL: `supabase/migrations/<NNN>_<description>.sql`
- Runner: `scripts/_migrate_<NNN>_<description>.js`
- Always wrap in `DO $$ BEGIN IF NOT EXISTS ... END $$` for idempotency
- Audit trigger: `CREATE TRIGGER ... AFTER INSERT OR UPDATE ... EXECUTE FUNCTION audit_trigger_func_v2()`
- Run against live DB after writing. Verify with `SELECT count(*)`.

### API route pattern
```typescript
import { withErrorHandler, withAuth } from '@/lib/api/middleware'
import { createSuccessResponse, ApiErrors } from '@/lib/api/errors'

export const GET = withErrorHandler(
  withAuth(async (request: NextRequest) => {
    return createSuccessResponse(data)
  }),
)
```

### Env var resolution (new names first, old as fallback)
```typescript
const url = process.env.INTAKE_SERVICE_URL || process.env.TENANT_APP_BASE_URL || 'http://localhost:8000'
```

### Contract freeze
- Never modify frozen contracts in-place. New version number for breaking changes.
- Contract registry: `INSERT ... ON CONFLICT (contract_key) DO NOTHING/UPDATE`

### RETAINER activation
- `GET /api/v1/matters/resolve-config?tenant_id=X` — snapshot all config
- `POST /api/v1/matters/activate` — 9 evidence refs validated, emits matter.activated
- `fn_upgrade_portal_access_on_activation()` — PROSPECTIVE_ENGAGEMENT → ACTIVE_MATTER

### Database gotchas
- `system_audit_log` has `log_id` not `id`; 15 columns, no `event_metadata`
- `audit_trigger_func_v2()`: actor_type must be `automated_job`, event_category must be `configuration`
- psql `\set` commands don't work with pg npm client — use inline JSON or `DO $$` blocks
- `contract_registry.contract_key` is UNIQUE

### NEVER expose .env.local secrets and keys in the IDE chat
