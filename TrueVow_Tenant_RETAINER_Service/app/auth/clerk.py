"""Supabase Auth JWT verification via truevow_auth.

In production (AUTH_MODE=supabase), tokens are validated against the Supabase JWKS endpoint
using the canonical truevow_auth library. In local/dev mode, tokens are verified with HS256
against LOCAL_JWT_SECRET.
"""

from __future__ import annotations

import jwt

from app.core.config import settings


def verify_token(token: str) -> dict:
    if settings.auth_mode == "supabase":
        from truevow_auth import verify_supabase_jwt

        payload = verify_supabase_jwt(token)
        if payload is None:
            raise jwt.PyJWTError("Supabase JWT verification failed.")
        return payload
    return jwt.decode(token, settings.local_jwt_secret, algorithms=[settings.local_jwt_algorithm])
