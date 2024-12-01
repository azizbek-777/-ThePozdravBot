from aiogram.types import CallbackQuery

from loader import dp
from utils.misc.set_birthday import set_birthday

@dp.callback_query_handler(text="edit_birthday")
async def edit_birthday(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await set_birthday(callback_query.message)