from typing import List

from aiogram.fsm.state import StatesGroup, State


class StateComplete(StatesGroup):
    search_cost = State()