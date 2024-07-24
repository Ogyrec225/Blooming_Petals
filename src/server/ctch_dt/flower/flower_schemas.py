import datetime
from typing import List
from pydantic import BaseModel


class FlowerCreate(BaseModel):
    flower: str


class FlowerReturn(FlowerCreate):
    id: int
