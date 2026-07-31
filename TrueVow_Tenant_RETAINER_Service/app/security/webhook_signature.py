"""WebhookSignature v1.0 — HMAC-SHA256 signing and verification.

Frozen contract. All TrueVow services use this same module for service-to-service
webhook authentication.

Canonical signing string: {timestamp_ms}:{METHOD}:{path}:{body_sha256}
"""

from __future__ import annotations

import hashlib
import hmac as hmac_module
import json
import logging
import time
from dataclasses import dataclass

logger = logging.getLogger("retainer.webhook_signature")

REPLAY_WINDOW_MS = 300_000
VALID_KEY_IDS = {"tv-primary"}
SIGNATURE_HEX_LENGTH = 64

# Per-service key registry — each key binds exactly one caller+receiver+path pair.
# No global fallback. A key accepted for INTAKE→RETAINER must not authorize RETAINER→SaaS Admin.
_KEY_REGISTRY: dict[str, dict] = {
    "tv-intake-to-retainer-v1": {
        "caller": "INTAKE",
        "paths": ["/api/v1/retainer/webhooks/candidate-submitted"],
        "methods": ["POST"],
    },
    "tv-intake-to-retainer-v2": {
        "caller": "INTAKE",
        "paths": ["/api/v1/retainer/webhooks/candidate-submitted"],
        "methods": ["POST"],
    },
    "tv-retainer-to-saas-admin-v1": {
        "caller": "RETAINER",
        "paths": ["/api/v1/matters/activate"],
        "methods": ["POST"],
    },
}


@dataclass
class VerifyResult:
    valid: bool
    key_id: str | None = None
    reason: str | None = None


def sign_request(
    method: str,
    path: str,
    body: bytes | str,
    key_id: str = "tv-primary",
    secret: str | None = None,
) -> dict[str, str]:
    """Sign a webhook request. Returns headers dict.

    Secret must be provided explicitly — no global fallback.
    Each caller-receiver pair has its own key.
    """
    if secret is None:
        raise ValueError(
            "Webhook secret is required. Each service-link has its own key. "
            "No global fallback. Set WEBHOOK_KEY_<KEY_ID> env var."
        )

    if isinstance(body, str):
        body = body.encode("utf-8")

    timestamp_ms = str(int(time.time() * 1000))
    body_hash = hashlib.sha256(body).hexdigest()
    signing_string = f"{timestamp_ms}:{method.upper()}:{path}:{body_hash}"
    signature = hmac_module.new(
        secret.encode("utf-8"), signing_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return {
        "X-TrueVow-Key-Id": key_id,
        "X-TrueVow-Timestamp": timestamp_ms,
        "X-TrueVow-Signature": signature,
    }


def verify_signature(
    headers: dict[str, str],
    method: str,
    path: str,
    raw_body: bytes,
    *,
    key_id_override: str | None = None,
    secret_override: str | None = None,
) -> VerifyResult:
    """Verify a WebhookSignature v1.0 request. Returns VerifyResult."""
    key_id = key_id_override or headers.get("x-truevow-key-id", "")
    timestamp_str = headers.get("x-truevow-timestamp", "")
    signature = headers.get("x-truevow-signature", "")

    if not key_id or not timestamp_str or not signature:
        return VerifyResult(valid=False, reason="MISSING_HEADERS")

    if not timestamp_str.isdigit():
        return VerifyResult(valid=False, key_id=key_id, reason="MALFORMED_TIMESTAMP")

    if not _valid_hex_signature(signature):
        return VerifyResult(valid=False, key_id=key_id, reason="INVALID_SIGNATURE_FORMAT")

    timestamp_ms = int(timestamp_str)
    now_ms = int(time.time() * 1000)
    if abs(now_ms - timestamp_ms) > REPLAY_WINDOW_MS:
        return VerifyResult(valid=False, key_id=key_id, reason="EXPIRED_TIMESTAMP")

    secret = _resolve_secret(key_id, secret_override)
    if secret is None:
        return VerifyResult(valid=False, key_id=key_id, reason="UNKNOWN_KEY_ID")

    registry_entry = _KEY_REGISTRY.get(key_id)
    if registry_entry:
        method_upper = method.upper()
        if method_upper not in registry_entry["methods"]:
            return VerifyResult(valid=False, key_id=key_id, reason="METHOD_NOT_ALLOWED")
        if path not in registry_entry["paths"]:
            return VerifyResult(valid=False, key_id=key_id, reason="PATH_NOT_ALLOWED")

    body_hash = hashlib.sha256(raw_body).hexdigest()
    method_upper = method.upper()
    signing_string = f"{timestamp_ms}:{method_upper}:{path}:{body_hash}"
    expected = hmac_module.new(
        secret.encode("utf-8"), signing_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    if not hmac_module.compare_digest(expected, signature):
        return VerifyResult(valid=False, key_id=key_id, reason="SIGNATURE_MISMATCH")

    return VerifyResult(valid=True, key_id=key_id)


def _resolve_secret(key_id: str, override: str | None = None) -> str | None:
    """Resolve a secret strictly by key_id from its dedicated env var.

    No global fallback. No universal key pool.
    Each key_id maps to exactly one env var: WEBHOOK_KEY_<KEY_ID>
    Example: tv-intake-to-retainer-v1 → WEBHOOK_KEY_TV_INTAKE_TO_RETAINER_V1
    """
    if override:
        return override

    if key_id not in _KEY_REGISTRY:
        return None

    import os

    env_var = f"WEBHOOK_KEY_{key_id.upper().replace('-', '_')}"
    secret = os.getenv(env_var)
    if secret:
        return secret

    # Check settings for structured config (production deployments)
    try:
        from app.core.config import settings

        keys = getattr(settings, "webhook_keys", None)
        if keys and isinstance(keys, dict) and key_id in keys:
            entry = keys[key_id]
            if isinstance(entry, dict):
                return entry.get("secret")
            return entry
    except Exception:
        pass

    return None


def _valid_hex_signature(sig: str) -> bool:
    if len(sig) != SIGNATURE_HEX_LENGTH:
        return False
    try:
        int(sig, 16)
        return True
    except ValueError:
        return False
