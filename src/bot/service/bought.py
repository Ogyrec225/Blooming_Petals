from aiogram import F, types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == "bought")
async def deliver(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Меню", callback_data="menu"))
    await callback.message.edit_text("Оплата проводится в оренах при конвертации 1 орена - 100 рублей. \n"
                                     "(В процессе разработки)", reply_markup=builder.as_markup())
