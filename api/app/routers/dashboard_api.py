import logging
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text
from app.database import get_db
from app.models import CallRecord
from app.middleware.auth import dashboard_auth

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dashboard")

@router.get("/metrics", dependencies=[Depends(dashboard_auth)])
async def get_metrics(db: AsyncSession = Depends(get_db)):
    """Compute metrics from our stored call records."""
    
    # Total calls
    result = await db.execute(select(func.count()).select_from(CallRecord))
    total_calls = result.scalar() or 0
    
    # Total offers (calls with an accepted load)
    result = await db.execute(
        select(func.count()).select_from(CallRecord).where(CallRecord.load_id.isnot(None))
    )
    total_offers = result.scalar() or 0
    
    # Average duration
    result = await db.execute(
        select(func.avg(CallRecord.duration_seconds)).select_from(CallRecord)
    )
    avg_duration = result.scalar() or 0
    
    # Outcome distribution
    result = await db.execute(
        select(CallRecord.outcome, func.count())
        .where(CallRecord.outcome.isnot(None))
        .group_by(CallRecord.outcome)
    )
    outcomes = {row[0]: row[1] for row in result.all()}
    
    # Sentiment distribution
    result = await db.execute(
        select(CallRecord.sentiment, func.count())
        .where(CallRecord.sentiment.isnot(None))
        .group_by(CallRecord.sentiment)
    )
    sentiments = {row[0]: row[1] for row in result.all()}
    
    # Booking rate (agreed / total_calls)
    booking_confirmed = outcomes.get("agreed", 0)
    booking_rate = (booking_confirmed / total_calls * 100) if total_calls else 0
    
    # Unverified carriers (outcome = not_eligible)
    result = await db.execute(
        select(func.count()).select_from(CallRecord).where(CallRecord.outcome == "not_eligible")
    )
    unverified_carriers = result.scalar() or 0
    
    # Loads not found
    result = await db.execute(
        select(func.count()).select_from(CallRecord).where(CallRecord.outcome == "no_match")
    )
    loads_not_found = result.scalar() or 0
    
    # Calls last 7 days
    result = await db.execute(
        select(
            func.date(CallRecord.created_at).label("date"),
            func.count().label("count")
        )
        .where(CallRecord.created_at >= func.now() - text("INTERVAL '7 days'"))
        .group_by(func.date(CallRecord.created_at))
        .order_by(func.date(CallRecord.created_at))
    )
    calls_last_7_days = [{"date": str(row[0]), "count": row[1]} for row in result.all()]
    
    return {
        "total_calls": total_calls,
        "total_offers": total_offers,
        "avg_duration_seconds": round(avg_duration, 1) if avg_duration else 0,
        "avg_duration_minutes": round(avg_duration / 60, 1) if avg_duration else 0,
        "outcomes": outcomes,
        "sentiments": sentiments,
        "booking_rate": round(booking_rate, 1),
        "unverified_carriers": unverified_carriers,
        "loads_not_found": loads_not_found,
        "calls_last_7_days": calls_last_7_days,
    }

@router.get("/calls", dependencies=[Depends(dashboard_auth)])
async def get_calls(db: AsyncSession = Depends(get_db)):
    """List all recorded calls for the calls table."""
    result = await db.execute(
        select(CallRecord).order_by(CallRecord.created_at.desc())
    )
    records = result.scalars().all()
    
    return [
        {
            "id": r.id,
            "run_id": r.run_id,
            "mc_number": r.mc_number,
            "carrier_name": r.carrier_name,
            "load_id": r.load_id,
            "origin": r.origin,
            "destination": r.destination,
            "equipment_type": r.equipment_type,
            "agreed_rate": r.agreed_rate,
            "initial_rate": r.initial_rate,
            "outcome": r.outcome,
            "sentiment": r.sentiment,
            "duration_seconds": r.duration_seconds,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "ended_at": r.ended_at.isoformat() if r.ended_at else None,
            "summary": r.summary,
            "loads_found": r.loads_found,
            "call_dropped": r.call_dropped,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]

@router.get("/calls/{run_id}", dependencies=[Depends(dashboard_auth)])
async def get_call_detail(run_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single call record detail."""
    result = await db.execute(select(CallRecord).where(CallRecord.run_id == run_id))
    r = result.scalar_one_or_none()
    
    if not r:
        return {"call": None, "offer": None, "summary": None}
    
    return {
        "call": {
            "id": r.id,
            "run_id": r.run_id,
            "duration_seconds": r.duration_seconds,
            "status": "completed" if r.ended_at else "started",
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "ended_at": r.ended_at.isoformat() if r.ended_at else None,
        },
        "offer": {
            "id": r.id,
            "mc_number": r.mc_number,
            "carrier_name": r.carrier_name,
            "load_id": r.load_id,
            "agreed_rate": r.agreed_rate,
            "initial_rate": r.initial_rate,
            "outcome": r.outcome,
            "sentiment": r.sentiment,
            "origin": r.origin,
            "destination": r.destination,
            "equipment_type": r.equipment_type,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        } if r.load_id else None,
        "summary": r.summary,
    }
