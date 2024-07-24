from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.send import send

router = Router()


@router.callback_query(F.data == "bought")
async def bought(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    answer = {"text": "Оплата проводится в оренах при конвертации 1 орена - 100 рублей. \n(В процессе разработки)",
              "reply_markup": builder.as_markup()}
    await send(callback, answer, state)
