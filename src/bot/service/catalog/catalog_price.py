import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.send import send
from src.bot.state import StateComplete

router = Router()


@router.callback_query(F.data == "search_cost")
async def search_cost(callback: types.CallbackQuery, state: FSMContext):
    logging.info("search_cost")
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    answer = {"text": "Какая максимальная цена за букет Вас устроит: ",
              "reply_markup": builder.as_markup()}
    await send(callback, answer, state)
    await state.set_state(StateComplete.search_cost)


@router.message(StateComplete.search_cost)
async def cost_catch(message: types.Message, state: FSMContext):
    await message.delete()
    builder = InlineKeyboardBuilder()
    if message.text.isnumeric():
        await state.update_data({"max_price": int(message.text)})
        max_price = (await state.get_data())["max_price"]

        builder.row(types.InlineKeyboardButton(text="Да", callback_data="catalog_flower"),
                    types.InlineKeyboardButton(text="Нет", callback_data="search_cost"))
        answer = {"text": f"Максимальная цена за букет {max_price}, верно?",
                  "reply_markup": builder.as_markup()}

    else:
        builder.row(types.InlineKeyboardButton(text="Ввести цену", callback_data="search_cost"))
        answer = {"text": "Пожалуйста, ведите цену в рублях.",
                  "reply_markup": builder.as_markup()}

    await send(message, answer, state)
    state_data = (await state.get_data())
    await state.clear()
    await state.set_data(state_data)

