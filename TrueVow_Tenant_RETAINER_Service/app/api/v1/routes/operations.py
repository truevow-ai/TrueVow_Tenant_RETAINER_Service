"""BP-06 Communications and BP-07 Activation API routes."""

# ruff: noqa: B008

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.deps import AuthContext, get_current_context
from app.core.database import get_db
from app.domain.activation import (
    authorize_activation,
    confirm_matter_activated,
    create_activation_checklist,
    evaluate_checklist_item,
)
from app.domain.communications import (
    create_reminder_schedule,
    expire_engagement,
    send_reminder,
    suppress_reminders,
)
from app.domain.hardening import get_workflow_health, validate_policy_compliance
from app.domain.trace_handoff import generate_trace_manifest
from app.domain.activation_client import send_activation_command
from app.models import (
    ActivationChecklist,
    ActivationChecklistItem,
    ReminderSchedule,
)
from app.schemas import (
    AuthorizeActivationResponse,
    ChecklistItemResponse,
    ConfirmActivationRequest,
    ConfirmActivationResponse,
    CreateChecklistRequest,
    CreateChecklistResponse,
    CreateReminderScheduleRequest,
    CreateReminderScheduleResponse,
    EvaluateItemRequest,
    EvaluateItemResponse,
    ExpireEngagementResponse,
    SendReminderRequest,
    SendReminderResponse,
)

router = APIRouter(tags=["operations"])


@router.post("/workflows/{workflow_id}/reminders", status_code=201, response_model=CreateReminderScheduleResponse)
async def create_reminder_endpoint(
    workflow_id: uuid.UUID,
    payload: CreateReminderScheduleRequest,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        sid = await create_reminder_schedule(
            db, workflow_id=workflow_id, tenant_id=uuid.UUID(ctx.firm_id),
            policy_version_id=payload.policy_version_id, max_attempts=payload.max_attempts,
            next_due_at=payload.next_due_at,
        )
        await db.commit()
        s = await db.get(ReminderSchedule, sid)
        return CreateReminderScheduleResponse(schedule_id=sid, state=s.state if s else "ACTIVE")
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.post("/reminders/{schedule_id}/send", status_code=201, response_model=SendReminderResponse)
async def send_reminder_endpoint(
    schedule_id: uuid.UUID,
    payload: SendReminderRequest,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        aid = await send_reminder(
            db, schedule_id=schedule_id, tenant_id=uuid.UUID(ctx.firm_id),
            communication_id=payload.communication_id, attempt_no=payload.attempt_no,
            result=payload.result,
        )
        await db.commit()
        return SendReminderResponse(attempt_id=aid, attempt_no=payload.attempt_no)
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.post("/reminders/{schedule_id}/suppress", status_code=200, response_model=CreateReminderScheduleResponse)
async def suppress_reminder_endpoint(
    schedule_id: uuid.UUID,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        sid = await suppress_reminders(db, schedule_id=schedule_id, tenant_id=uuid.UUID(ctx.firm_id))
        await db.commit()
        s = await db.get(ReminderSchedule, sid)
        return CreateReminderScheduleResponse(schedule_id=sid, state=s.state if s else "SUPPRESSED")
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.post("/workflows/{workflow_id}/expire", status_code=200, response_model=ExpireEngagementResponse)
async def expire_endpoint(
    workflow_id: uuid.UUID,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        wid = await expire_engagement(db, workflow_id=workflow_id, tenant_id=uuid.UUID(ctx.firm_id))
        await db.commit()
        return ExpireEngagementResponse(workflow_id=wid, state="DECLINED_OR_EXPIRED")
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.post("/workflows/{workflow_id}/activation-checklist", status_code=201, response_model=CreateChecklistResponse)
async def create_checklist_endpoint(
    workflow_id: uuid.UUID,
    payload: CreateChecklistRequest,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        items = [i.model_dump() for i in payload.items]
        cid = await create_activation_checklist(
            db, workflow_id=workflow_id, tenant_id=uuid.UUID(ctx.firm_id),
            policy_version_id=payload.policy_version_id, items=items,
        )
        await db.commit()
        cl = await db.get(ActivationChecklist, cid)
        item_result = await db.execute(
            select(ActivationChecklistItem).where(ActivationChecklistItem.checklist_id == cid)
        )
        it = item_result.scalars().all()
        return CreateChecklistResponse(
            checklist_id=cid, state=cl.state if cl else "PENDING",
            items=[ChecklistItemResponse(**i.__dict__) for i in it],
        )
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.post("/checklist-items/{item_id}/evaluate", status_code=200, response_model=EvaluateItemResponse)
async def evaluate_item_endpoint(
    item_id: uuid.UUID,
    payload: EvaluateItemRequest,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        iid = await evaluate_checklist_item(
            db, item_id=item_id, tenant_id=uuid.UUID(ctx.firm_id),
            result=payload.result, evidence_refs=payload.evidence_refs,
        )
        await db.commit()
        return EvaluateItemResponse(item_id=iid, result=payload.result)
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.post("/checklists/{checklist_id}/authorize", status_code=200, response_model=AuthorizeActivationResponse)
async def authorize_activation_endpoint(
    checklist_id: uuid.UUID,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        cid = await authorize_activation(
            db, checklist_id=checklist_id, tenant_id=uuid.UUID(ctx.firm_id),
            attorney_actor_id=ctx.user_id,
        )
        await db.commit()
        cl = await db.get(ActivationChecklist, cid)
        return AuthorizeActivationResponse(checklist_id=cid, state=cl.state if cl else "AUTHORIZED")
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.post("/workflows/{workflow_id}/activate", status_code=200, response_model=ConfirmActivationResponse)
async def confirm_activation_endpoint(
    workflow_id: uuid.UUID,
    payload: ConfirmActivationRequest,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        wid = await confirm_matter_activated(
            db, workflow_id=workflow_id, tenant_id=uuid.UUID(ctx.firm_id),
            activated_matter_id=payload.activated_matter_id,
        )
        await db.commit()
        return ConfirmActivationResponse(
            workflow_id=wid, state="ACTIVATED", activated_matter_id=payload.activated_matter_id,
        )
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.get("/workflows/{workflow_id}/trace-manifest")
async def trace_manifest_endpoint(
    workflow_id: uuid.UUID,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        manifest = await generate_trace_manifest(
            db, workflow_id=workflow_id, tenant_id=uuid.UUID(ctx.firm_id),
        )
        await db.commit()
        return manifest
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=409, detail=str(e)) from None


@router.get("/workflows/{workflow_id}/policy-compliance")
async def policy_compliance_endpoint(
    workflow_id: uuid.UUID,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await validate_policy_compliance(
            db, workflow_id=workflow_id, tenant_id=uuid.UUID(ctx.firm_id),
        )
        await db.commit()
        return result
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=404, detail=str(e)) from None


@router.get("/workflows/{workflow_id}/health")
async def workflow_health_endpoint(
    workflow_id: uuid.UUID,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await get_workflow_health(
            db, workflow_id=workflow_id, tenant_id=uuid.UUID(ctx.firm_id),
        )
        await db.commit()
        return result
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=404, detail=str(e)) from None


@router.post("/workflows/{workflow_id}/activate-to-saas-admin", status_code=202)
async def activate_to_saas_admin_endpoint(
    workflow_id: uuid.UUID,
    ctx: AuthContext = Depends(get_current_context),
    db: AsyncSession = Depends(get_db),
):
    """Sign and send the ActivateMatterCommand to SaaS Admin."""
    from app.core.config import settings
    from app.domain.activation import confirm_matter_activated

    saas_url = getattr(settings, "saas_admin_url", None) or "http://localhost:3001"
    secret = getattr(settings, "intake_webhook_secret", None) or settings.service_api_key

    try:
        # Gather activation evidence
        wf = await db.get(RetainerWorkflow, workflow_id)
        if wf is None or str(wf.tenant_id) != ctx.firm_id:
            raise HTTPException(status_code=404, detail="Workflow not found")

        payload = {
            "tenant_id": str(wf.tenant_id),
            "engagement_workflow_id": str(workflow_id),
            "representation_decision_id": str(wf.representation_decision_id) if wf.representation_decision_id else None,
            "conflict_review_id": str(wf.conflict_review_id) if wf.conflict_review_id else None,
            "engagement_package_id": str(wf.engagement_package_id) if wf.engagement_package_id else None,
            "activation_checklist_id": str(wf.activation_checklist_id) if wf.activation_checklist_id else None,
            "activated_matter_id": str(wf.activated_matter_id) if wf.activated_matter_id else str(uuid.uuid4()),
            "command_id": str(uuid.uuid4()),
        }

        result = await send_activation_command(saas_url, payload, webhook_secret=secret)
        await db.commit()

        if result["success"]:
            return {"status": "accepted", "saas_admin_response": result.get("data")}
        return {"status": "failed", "error": result.get("error")}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=502, detail=str(e)) from None
