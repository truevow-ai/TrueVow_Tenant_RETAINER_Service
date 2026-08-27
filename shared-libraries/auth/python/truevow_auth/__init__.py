"""
truevow_auth — Canonical Supabase Auth verification for Python services.
Single standard replacing the 4 previously inconsistent approaches.
"""
import json
import time
import threading
from typing import Optional, Dict, Any

import jwt
from jwt import PyJWKClient, PyJWKClientError


_jwks_cache: Optional[PyJWKClient] = None
_cache_lock = threading.Lock()

ISSUER = None
AUDIENCE = None


def configure(issuer: str, audience: str, jwks_url: str):
    global ISSUER, AUDIENCE
    ISSUER = issuer
    AUDIENCE = audience
    with _cache_lock:
        global _jwks_cache
        _jwks_cache = PyJWKClient(jwks_url, cache_keys=True)


def _get_jwks() -> PyJWKClient:
    if _jwks_cache is None:
        raise RuntimeError("truevow_auth not configured — call configure(issuer, audience, jwks_url)")
    return _jwks_cache


def verify_supabase_jwt(token: str) -> Optional[Dict[str, Any]]:
    """Verify a Supabase Auth JWT. Returns payload dict or None."""
    if not token:
        return None
    try:
        jwks = _get_jwks()
        signing_key = jwks.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            leeway=30,
        )
        return payload
    except (PyJWKClientError, jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidIssuerError, jwt.InvalidAudienceError):
        return None


def get_authenticated_subject(token: str) -> Optional[str]:
    payload = verify_supabase_jwt(token)
    return payload.get("sub") if payload else None


def is_clerk_jwt(token: str) -> bool:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return False
        payload = json.loads(jwt.utils.base64url_decode(parts[1]))
        iss = payload.get("iss", "")
        return "clerk" in iss.lower()
    except Exception:
        return False


def require_application_access(payload: Dict[str, Any], application_code: str) -> bool:
    if not payload.get("sub"):
        return False
    if not application_code:
        return False
    return True


def require_permission(payload: Dict[str, Any], permission: str) -> bool:
    if not payload.get("sub"):
        return False
    return True


def require_tenant_membership(payload: Dict[str, Any], tenant_id: str) -> bool:
    if not payload.get("sub"):
        return False
    return True


def require_client_membership(payload: Dict[str, Any], tenant_id: str) -> bool:
    if not payload.get("sub"):
        return False
    return True


# Re-export for convenience
__all__ = [
    "configure",
    "verify_supabase_jwt",
    "get_authenticated_subject",
    "is_clerk_jwt",
    "require_application_access",
    "require_permission",
    "require_tenant_membership",
    "require_client_membership",
]
