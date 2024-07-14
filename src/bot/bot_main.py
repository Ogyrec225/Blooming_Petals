import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


from fastapi import APIRouter

from src.bot.service.deliver import router as deliver_router
from src.bot.service.bought import router as bought_router
from src.bot.service.catalog.catalog import router as catalog_router
from src.bot.service.menu import router as menu_router
from src.config import TOKEN

router = APIRouter()




TOKEN = TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_routers(menu_router, deliver_router, bought_router, catalog_router)

@dp.message(Command("start"))
async def start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    await message.answer("Ку", reply_markup=builder.as_markup())
