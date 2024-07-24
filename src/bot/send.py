import logging

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


async def send(message: Message | CallbackQuery, answer: dict, state: FSMContext):
    last_message = (await state.get_data())["last_message"]
    logging.info(last_message)
    if message is CallbackQuery:
        message = message.message
    try:
        await state.update_data(last_message=(await last_message.edit_text(**answer)))
    except TelegramBadRequest:
        last_message = (await message.answer(**answer))
        try:
            await last_message.delete()
            await state.update_data(last_message=last_message)
        except AttributeError:
            await state.update_data(last_message=(await message.answer(**answer)))

