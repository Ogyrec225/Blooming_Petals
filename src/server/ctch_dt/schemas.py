import datetime
from typing import List
from pydantic import BaseModel


class BouquetCreate(BaseModel):
    bouquet_name: str
    photo_address: str
    type_flowers: List[str]
    cost: int
    count: int


class BouquetReturn(BouquetCreate):
    id: int
    add_at: datetime.datetime
