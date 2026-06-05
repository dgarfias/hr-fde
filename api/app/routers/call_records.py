from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import CallRecord
from app.schemas import CallRecordCreate, CallRecordResponse
from app.middleware.auth import api_key_auth
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/calls", tags=["Calls"])

@router.post("/record", response_model=CallRecordResponse, status_code=201)
async def record_call(
    request: CallRecordCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(api_key_auth),
):
    """Record a complete call at the end of the conversation.
    
    The HappyRobot workflow should POST here after the voice agent ends.
    All fields are optional except run_id and outcome.
    """
    
    # Check if already recorded
    result = await db.execute(select(CallRecord).where(CallRecord.run_id == request.run_id))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Call already recorded")
    
    db_record = CallRecord(**request.model_dump())
    db.add(db_record)
    await db.commit()
    await db.refresh(db_record)
    logger.info(f"Recorded call {request.run_id} outcome={request.outcome}")
    return db_record

@router.get("/record", response_model=list[CallRecordResponse])
async def list_records(
    db: AsyncSession = Depends(get_db),
    _=Depends(api_key_auth),
    limit: int = 100,
):
    """List all recorded calls."""
    result = await db.execute(
        select(CallRecord).order_by(CallRecord.created_at.desc()).limit(limit)
    )
    return result.scalars().all()
