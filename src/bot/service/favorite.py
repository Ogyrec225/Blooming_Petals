from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.send import send

router = Router()


@router.callback_query(F.data == "favorite")
async def favorite(callback: types.CallbackQuery, state: FSMContext):
    text = "В разработке"
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    answer = {"text": text, "reply_markup": builder.as_markup()}
    await send(callback, answer, state)
