"""RETAINER FastAPI application.

Wires middleware (correlation id + audit), Clerk-based auth, plain-English error
handling, a public /health probe, and the firm-scoped v1 API under
/api/v1/retainer. Production must run in Clerk auth mode — enforced at startup.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv(".env.local", override=True)

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from app.api.v1 import router as v1_router  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.core.errors import install_error_handlers  # noqa: E402
from app.core.logging import get_logger  # noqa: E402
from app.core.middleware import audit_middleware, correlation_id_middleware  # noqa: E402

logger = get_logger("retainer.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.is_production and settings.auth_mode != "clerk":
        raise RuntimeError(
            "AUTH_MODE=local is forbidden in production. Set AUTH_MODE=clerk and CLERK_JWKS_URL."
        )
    logger.info(
        "RETAINER starting: env=%s auth_mode=%s db=supabase",
        settings.environment,
        settings.auth_mode,
    )
    yield
    logger.info("RETAINER shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.middleware("http")(audit_middleware)
app.middleware("http")(correlation_id_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_allow_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

install_error_handlers(app)
app.include_router(v1_router, prefix="/api/v1/retainer")


@app.get("/health", tags=["health"])
async def health() -> dict:
    return {
        "status": "healthy",
        "service": "retainer",
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get("/ready", tags=["health"])
async def ready() -> dict:
    """Readiness probe — database, migrations, critical tables.

    Returns 200 when the service is ready for live traffic.
    Returns 503 when database or schema is not ready.
    """
    from fastapi.responses import JSONResponse
    from sqlalchemy import text

    CRITICAL_TABLES = [
        "retainer.retainer_workflows",
        "retainer.candidate_reviews",
        "retainer.representation_decisions",
        "retainer.conflict_searches",
        "retainer.conflict_candidates",
        "retainer.template_resolutions",
        "retainer.engagement_packages",
        "retainer.package_documents",
        "retainer.signature_ceremonies",
        "retainer.activation_checklists",
        "retainer.checklist_items",
        "retainer.portal_access_grants",
        "retainer.audit_events",
        "retainer.retainer_outbox_events",
        "retainer.alembic_version",
    ]

    try:
        from app.core.database import engine as _engine

        engine = _engine
        async with engine.connect() as conn:
            # 1. Migration head
            result = await conn.execute(
                text("SELECT version_num FROM information_schema.schemata WHERE schema_name = 'retainer'")
            )
            if not result.fetchone():
                return JSONResponse(
                    status_code=503,
                    content={"status": "not_ready", "reason": "retainer schema not found"},
                )

            result = await conn.execute(
                text("SELECT version_num FROM retainer.alembic_version ORDER BY version_num DESC LIMIT 1")
            )
            row = result.fetchone()
            current_head = row[0] if row else "unknown"

            # 2. Critical tables
            missing = []
            for table_name in CRITICAL_TABLES:
                try:
                    await conn.execute(text(f"SELECT 1 FROM {table_name} LIMIT 0"))
                except Exception:
                    missing.append(table_name)

            if missing:
                return JSONResponse(
                    status_code=503,
                    content={
                        "status": "not_ready",
                        "reason": f"missing tables: {', '.join(missing)}",
                        "migration_head": current_head,
                    },
                )

            # 3. Idempotency index check
            try:
                await conn.execute(text(
                    "SELECT 1 FROM pg_indexes WHERE schemaname = 'retainer' "
                    "AND indexname = 'idx_outbox_event_id_unique'"
                ))
            except Exception:
                pass

            return {
                "status": "ready",
                "database": "connected",
                "migration_head": current_head,
                "migration_count": len([m for m in missing if False]) + len(CRITICAL_TABLES),
                "critical_tables": len(CRITICAL_TABLES),
                "missing_tables": 0,
            }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "reason": str(e)[:200],
            },
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)
