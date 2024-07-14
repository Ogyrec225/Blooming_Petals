from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "menu")
async def menu(querry: types.CallbackQuery, state: FSMContext):
    await state.clear()
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Оформить заказ", callback_data="bought"),
                types.InlineKeyboardButton(text="Доставка", callback_data="deliver"))

    builder.row(types.InlineKeyboardButton(text="Избранное", callback_data="favorite"),
                types.InlineKeyboardButton(text="Поиск по бюджету", callback_data="search_cost"))
    builder.row(types.InlineKeyboardButton(text="Каталог", callback_data="catalog"))
    await querry.message.edit_text("Что-то о магазине", reply_markup=builder.as_markup())  # Type CallbackQuerry
