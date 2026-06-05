from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database import get_db
from app.models import Load
from app.schemas import LoadResponse, LoadSearchParams
from app.services.load_service import search_loads
from app.schemas import LoadMatchResponse

router = APIRouter()

@router.get("/match", response_model=LoadMatchResponse)
async def match_load(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    equipment_type: Optional[str] = Query(None),
    pickup_date: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
):
    """Return matching loads as a flat object with an embedded array.

    Designed for voice agent tools: single top-level object with a `found`
    flag (like VerifyMC), but includes up to 3 loads so the agent can
    pitch alternatives if the carrier asks.
    """
    params = LoadSearchParams(
        origin=origin,
        destination=destination,
        equipment_type=equipment_type,
        pickup_date=pickup_date,
    )
    results = await search_loads(db, params, limit=3)
    if not results:
        return LoadMatchResponse(found=False)

    loads = [
        {
            "load_id": r.load_id,
            "origin": r.origin,
            "destination": r.destination,
            "pickup_datetime": r.pickup_datetime,
            "delivery_datetime": r.delivery_datetime,
            "equipment_type": r.equipment_type,
            "loadboard_rate": r.loadboard_rate,
            "miles": r.miles,
            "notes": r.notes,
        }
        for r in results
    ]

    return LoadMatchResponse(
        found=True,
        count=len(loads),
        loads=loads,
    )

@router.get("", response_model=list[LoadResponse])
async def list_loads(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    equipment_type: Optional[str] = Query(None),
    pickup_date: Optional[str] = Query(None, description="Format: YYYY-MM-DD"),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    params = LoadSearchParams(
        origin=origin,
        destination=destination,
        equipment_type=equipment_type,
        pickup_date=pickup_date,
    )
    return await search_loads(db, params, limit)

@router.get("/{load_id}", response_model=LoadResponse)
async def get_load(load_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Load).where(Load.load_id == load_id))
    load = result.scalar_one_or_none()
    if not load:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Load not found")
    return load
