import logging
from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, func, or_, and_, false, true, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.server.ctch_dt.bouquet.bouquet_model import bouquet
from src.server.ctch_dt.bouquet.bouquet_schemas import BouquetCreate, BouquetReturn, BouquetFilter

from datetime import datetime

router = APIRouter(
    prefix="/bouquet",
    tags=["bouquet"]
)


@router.post("/add/{bouquet_name}")
async def add_bouquet_data(new_bouquet: BouquetCreate, session: AsyncSession = Depends(get_async_session)) -> Dict:
    try:
        stmt = insert(bouquet).values(id=(await session.execute(
            select(func.max(bouquet.c.id)))
                                          ).first()[0] + 1,
                                      **(new_bouquet.dict()),
                                      add_at=datetime.now()
                                      )
    except TypeError:
        stmt = insert(bouquet).values(id=0,
                                      **(new_bouquet.dict()),
                                      add_at=datetime.now()
                                      )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.get("/show/{bouquet_id}")
async def get_bouquet_data(bouquet_id: int,
                           session: AsyncSession = Depends(get_async_session)) \
        -> BouquetReturn | Dict:
    query = select(bouquet).where(bouquet.c.id == bouquet_id)
    result = (await session.execute(query)).all()
    try:
        return result[0]
    except IndexError:
        return {
            "error": "IndexError",
            "code_error": 204,
            "err_message": f"Not found bouquet with id:{bouquet_id}"
        }


@router.delete("/delete/{bouquet_id}")
async def del_bouquet(bouquet_id: int, session: AsyncSession = Depends(get_async_session)) -> Dict:
    row_delete = (await session.execute(delete(bouquet).where(bouquet.c.id == bouquet_id))).rowcount()
    if row_delete > 0:
        return {"error": "Ok",
                "code_error": 200}
    else:
        return {"error": "Row wasn't delete, maybe not found",
                "code_error": 205}


@router.post("/get_filter")
async def get_filter_data(bouquet_filter_data: BouquetFilter, bouquet_id: int = 0,
                          session: AsyncSession = Depends(get_async_session)) -> Dict[BouquetReturn, int] | Dict:
    querry = select(bouquet)

    result = (await session.execute(querry.where(
        and_(
            or_(false(), *[func.array_position(bouquet.c.type_flowers, flower) is not None
                           for flower in bouquet_filter_data.flower_list]),
            bouquet.c.price < bouquet_filter_data.max_price if bouquet_filter_data.max_price > 0
            else true(),
            bouquet.c.count > 0 if bouquet_filter_data.is_available else true()
        )
    )
                                    if (
                (len(bouquet_filter_data.flower_list) > 0) | (bouquet_filter_data.max_price > 0))
                                    else querry)
              ).all()
    try:
        return {"result": result[bouquet_id], "all_rows": len(result)}
    except IndexError:
        return {
            "error": "IndexError",
            "code_error": 204,
            "err_message": f"Not found bouquet with id:{bouquet_id}",
            "filter_data_flowers": bouquet_filter_data.flower_list,
            "filter_data_cost": bouquet_filter_data.max_price
        }
