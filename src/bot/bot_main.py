import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


from src.bot.service.deliver import router as deliver_router
from src.bot.service.bought import router as bought_router
from src.bot.service.catalog.catalog_price import router as catalog_price_router
from src.bot.service.catalog.catalog_flower import router as catalog_flower_router
from src.bot.service.menu import router as menu_router
from src.bot.service.catalog.catalog_show import router as catalog_show_router
from src.config import TOKEN



TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_routers(menu_router, bought_router, deliver_router,
                   catalog_show_router, catalog_price_router, catalog_flower_router)


@dp.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data({"id": 0,
                             "page": 1,
                             "max_cost": 0,
                             "flower_list": []})
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    await state.update_data(last_message=(await message.answer("Ку", reply_markup=builder.as_markup())))
