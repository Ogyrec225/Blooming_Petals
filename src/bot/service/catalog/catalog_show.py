import logging
from os.path import join

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.service.bought import bought
from src.bot.service.menu import menu
from src.database import async_session_maker
from src.server.ctch_dt.bouquet.bouquet_schemas import BouquetFilter
from src.server.ctch_dt.bouquet.router_bouquet import get_filter_data

router = Router()


#TODO Содержание сообщение: фото цветка, цена, описание.
# Кнопки:
#                  купить
# Optional[предидущий  следующий]
#                   меню
# запрос к базе, поиск фото
@router.callback_query(F.data.startswith("catalog_show"))
async def catalog(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()

    data = (await state.get_data())
    async with async_session_maker() as session:
        filter_data = (await get_filter_data(BouquetFilter(flower_list=data["flower_list"],
                                                           max_cost=data["max_cost"],
                                                           is_available=True),
                                             bouquet_id=data["id"],
                                             session=session))  #value
        bouquet_data = dict(zip(["bouquet_name", "description", "photo_address", "type_flowers", "price"],
                                filter_data["result"][1:6]))  # keys

        text = f"{bouquet_data["bouquet_name"]}.\n\n {bouquet_data["description"]}\n\nЦена: {bouquet_data["price"]} рублей."
        photo = FSInputFile(join("src", "server", "data", bouquet_data["photo_address"]))

    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="catalog_return_menu"))
    buttons = []
    if data["id"] > 0:
        buttons.append(types.InlineKeyboardButton(text="Предыдущий", callback_data="catalog_show_prev"))
    if data["id"] < (filter_data["all_rows"] - 1):
        buttons.append(types.InlineKeyboardButton(text="Следующий", callback_data="catalog_show_next"))
    if len(buttons) > 0:
        builder.row(*buttons)
    builder.row(types.InlineKeyboardButton(text="Купить", callback_data="catalog_return_bought"))

    await callback.message.delete()
    await callback.message.answer_photo(caption=text,
                                        photo=photo,
                                        reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("catalog_return"))
async def catalog_return(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    if callback.data == "catalog_return_menu":
        await menu(callback, state)
    else:
        await state.clear()
        await bought(callback)
