import logging

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.send import send
from src.bot.service.menu import menu
from src.database import async_session_maker
from src.server.ctch_dt.flower.router_flower import flower_get_all

router = Router()


@router.callback_query(F.data == "catalog_flower")
async def catalog_flower(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    full_buttons = True
    try:
        page = (await state.get_data())["page"]
    except KeyError:
        await menu(callback,state)
    else:
        async with async_session_maker() as session:
            flowers = await flower_get_all(start_value=(page - 1) * 4, end_value=page * 4, session=session)

            for flower_id in range((page - 1) * 4, page * 4, 2):
                row = []
                try:
                    row.append(types.InlineKeyboardButton(text=flowers[flower_id],
                                                          callback_data=f"flower_{flowers[flower_id]}"))
                    row.append(types.InlineKeyboardButton(text=flowers[flower_id + 1],
                                                          callback_data=f"flower_{flowers[flower_id + 1]}"))
                except IndexError:
                    full_buttons = False
                    break
                finally:
                    builder.row(*row)
                    del row

            buttons = []
            if page > 1:
                buttons.append(types.InlineKeyboardButton(text="Предидущая", callback_data="catalog_flower_prev"))
            if full_buttons:
                buttons.append(types.InlineKeyboardButton(text="Следующая", callback_data="catalog_flower_next"))
            builder.row(*buttons)

            builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
            builder.row(types.InlineKeyboardButton(text="Продолжить", callback_data="catalog_show"))

        change_flowers = (await state.get_data())["flower_list"]

        text = "\nВыбранных цветов нет."
        if len(change_flowers) > 0:
            text = "\nВыбранные цветы: "
            for flower in change_flowers:
                text += flower.lower() + " "

        answer = {"text": "Выберете цветы, которые хотите видеть в букете." + text,
                  "reply_markup": builder.as_markup()}
        await send(callback, answer, state)


@router.callback_query(F.data.startswith("flower_"))
async def flower_handler(callback: types.CallbackQuery, state: FSMContext):
    flower_list = (await state.get_data())["flower_list"]
    if callback.data[7:] not in flower_list:
        flower_list.append(callback.data[7:])
    await state.update_data({"flower_list": flower_list})
    await catalog_flower(callback, state)


@router.callback_query(F.data == "catalog_flower_prev")
async def catalog_flower_prev(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data({"page": (await state.get_data())["page"] - 1})
    await catalog_flower(callback, state)


@router.callback_query(F.data == "catalog_flower_next")
async def catalog_flower_prev(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data({"page": (await state.get_data())["page"] + 1})
    await catalog_flower(callback, state)
