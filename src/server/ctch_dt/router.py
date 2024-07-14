from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.server.ctch_dt.model import bouquet
from src.server.ctch_dt.schemas import BouquetCreate, BouquetReturn

from datetime import datetime

router = APIRouter(
    prefix="/bouquet",
    tags=["bouquet"]
)


@router.get("/show/{bouquet_name}")
async def get_bouquet_data(bouquet_name: str,
                           session: AsyncSession = Depends(get_async_session))\
        -> List[BouquetReturn]:
    query = select(bouquet).where(bouquet.c.bouquet_name == bouquet_name)
    result = await session.execute(query)
    return result.all()


@router.post("/add/{bouquet_name}")
async def add_bouquet_data(new_bouquet: BouquetCreate, session: AsyncSession = Depends(get_async_session)) -> Dict:
    stmt = insert(bouquet).values(id=(await session.execute(
        select(func.max(bouquet.c.id)))
                                      ).first()[0]+1,
                                  **(new_bouquet.dict()),
                                  add_at=datetime.now())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
