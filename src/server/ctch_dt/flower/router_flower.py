from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import insert, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.server.ctch_dt.flower.flower_model import flower
from src.server.ctch_dt.flower.flower_schemas import FlowerCreate, FlowerReturn

router = APIRouter(
    prefix="/flower",
    tags=["flower"]
)


@router.post('/{flower_id}/add')
async def flower_add(new_flower: FlowerCreate, session: AsyncSession = Depends(get_async_session)) -> Dict:
    try:
        stmt = insert(flower).values(id=(await session.execute(
            select(func.max(flower.c.id)))
                                          ).first()[0] + 1,
                                      **(new_flower.dict())
                                      )
    except TypeError:
        stmt = insert(flower).values(id=0,
                                      **(new_flower.dict())
                                      )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/{flower_id}/get")
async def flower_get(flower_id:int, session: AsyncSession = Depends(get_async_session)) -> FlowerReturn|Dict:
    querry = select(flower).where(flower.c.id == flower_id)
    result = (await session.execute(querry)).all()
    try:
        return result[0]
    except IndexError:
        return {
            "error": "IndexError",
            "code_error": 204,
            "err_message": f"Not found flower with id:{flower_id}"
        }


@router.get("/get/all_flower")
async def flower_get_all(start_value: int = None, end_value: int = None, session: AsyncSession = Depends(get_async_session)) -> List[str]:
    result = list(
        map(lambda tuple: tuple[0],
                 ((await session.execute(select(flower.c.flower))).all())))
    if slice is not None:
        return result[start_value:end_value]
    else:
        return result