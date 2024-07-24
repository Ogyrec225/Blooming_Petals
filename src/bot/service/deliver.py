from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.send import send

router = Router()


@router.callback_query(F.data == "deliver")
async def deliver(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    answer = {"text": "Доставляем по всей Ривии. По всем вопросам обращаться на почту. \n(В процессе разработки)",
              "reply_markup": builder.as_markup()}
    await send(callback, answer, state)
