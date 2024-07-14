from aiogram import types, F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "deliver")
async def deliver(querry: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    await querry.message.edit_text("Доставляем по всей Ривии. По всем вопросам обращаться на почту. \n"
                                "(В процессе разработки)", reply_markup=builder.as_markup())
