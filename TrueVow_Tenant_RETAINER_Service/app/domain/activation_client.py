"""RETAINER → SaaS Admin activation client — signs and sends ActivateMatterCommand."""

from __future__ import annotations

import json
import logging
import uuid

import httpx

from app.security.webhook_signature import sign_request

logger = logging.getLogger("retainer.activation_client")

SAAS_ADMIN_ACTIVATE_PATH = "/api/v1/matters/activate"
RETAINER_KEY_ID = "tv-retainer-to-saas-admin-v1"


async def send_activation_command(
    saas_admin_url: str,
    payload: dict,
    *,
    webhook_secret: str,
    timeout: float = 30.0,
) -> dict:
    body = json.dumps(payload)
    headers = sign_request(
        "POST",
        SAAS_ADMIN_ACTIVATE_PATH,
        body,
        key_id=RETAINER_KEY_ID,
        secret=webhook_secret,
    )
    headers["Content-Type"] = "application/json"
    headers["X-Tenant-Id"] = str(payload.get("tenant_id", ""))
    headers["X-Correlation-Id"] = str(uuid.uuid4())

    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{saas_admin_url.rstrip('/')}{SAAS_ADMIN_ACTIVATE_PATH}"
        response = await client.post(url, content=body, headers=headers)

        if response.status_code in (200, 201):
            return {"success": True, "status": response.status_code, "data": response.json()}

        logger.warning(
            "Activation request failed: status=%s body=%s",
            response.status_code,
            response.text[:500],
        )
        return {"success": False, "status": response.status_code, "error": response.text[:500]}
