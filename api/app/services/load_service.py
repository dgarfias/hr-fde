from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models import Load
from app.schemas import LoadSearchParams

async def search_loads(db: AsyncSession, params: LoadSearchParams, limit: int = 50):
    query = select(Load)
    filters = []
    if params.origin:
        filters.append(Load.origin.ilike(f"%{params.origin}%"))
    if params.destination:
        filters.append(Load.destination.ilike(f"%{params.destination}%"))
    if params.equipment_type:
        filters.append(Load.equipment_type.ilike(f"%{params.equipment_type}%"))
    if params.pickup_date:
        try:
            date_obj = datetime.strptime(params.pickup_date, "%Y-%m-%d")
            filters.append(
                and_(
                    Load.pickup_datetime >= date_obj,
                    Load.pickup_datetime < date_obj + timedelta(days=1),
                )
            )
        except ValueError:
            pass
    if filters:
        query = query.where(and_(*filters))
    query = query.limit(limit)
    result = await db.execute(query)
    return result.scalars().all()
