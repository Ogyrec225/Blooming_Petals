import logging

from aiogram import types, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


@router.callback_query(F.data == "menu")
async def menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_data({"id": 0,
                             "page": 1,
                             "max_cost": 0,
                             "flower_list": []})
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Оформить заказ", callback_data="bought"),
                types.InlineKeyboardButton(text="Доставка", callback_data="deliver"))

    builder.row(types.InlineKeyboardButton(text="Избранное", callback_data="favorite"),
                types.InlineKeyboardButton(text="Поиск по бюджету", callback_data="search_cost"))
    builder.row(types.InlineKeyboardButton(text="Каталог", callback_data="catalog_flower"))
    answer = {"text": "Что-то о магазине",
              "reply_markup": builder.as_markup()}

    try:
        await state.update_data(last_message=(await callback.message.edit_text(**answer)))
    except TelegramBadRequest:
        await state.update_data(last_message=(await callback.message.answer(**answer)))
