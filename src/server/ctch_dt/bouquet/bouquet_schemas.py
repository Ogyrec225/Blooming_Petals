import datetime
from typing import List
from pydantic import BaseModel


class BouquetCreate(BaseModel):
    bouquet_name: str
    description: str
    photo_address: str
    type_flowers: List[str]
    price: int
    count: int


class BouquetReturn(BouquetCreate):
    id: int
    add_at: datetime.datetime


class BouquetFilter(BaseModel):
    flower_list: List[str]
    max_price: float = 0
    is_available: bool = False
