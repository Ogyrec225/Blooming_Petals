from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Cost(StatesGroup):
    search_cost = State()
    max_price: int = -1


router = Router()


@router.callback_query(F.data == "search_cost")
async def search_cost(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    await callback.message.edit_text("Какая максимальная цена за букет Вас устроит: ", reply_markup=builder.as_markup())
    await state.set_state(Cost.search_cost)


@router.message(Cost.search_cost)
async def cost_catch(message: types.Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    if message.text.isnumeric():
        await state.set_data({"max_price": int(message.text)})
        max_price = (await state.get_data())["max_price"]
        builder.row(types.InlineKeyboardButton(text="Да", callback_data="catalog"),
                    types.InlineKeyboardButton(text="Нет", callback_data="search_cost"))
        await message.answer(f"Максимальная цена за букет {max_price}, верно?", reply_markup=builder.as_markup())

    else:
        builder.row(types.InlineKeyboardButton(text="Ввести цену", callback_data="search_cost"))
        await message.answer(f"Пожалуйста, ведите цену в рублях.", reply_markup=builder.as_markup())



@router.callback_query(F.data == "catalog")
async def catalog(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))

    if len((await state.get_data())) == 0:
        await callback.message.edit_text(f"Максимальной цены за букет нет.", reply_markup=builder.as_markup())

    else:
        max_price = (await state.get_data())["max_price"]
        await state.clear()
        await callback.message.edit_text(f"Максимальная цена за букет {max_price}.", reply_markup=builder.as_markup())
