from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.misc.set_birthday import set_birthday

@dp.callback_query_handler(text="edit_birthday")
async def edit_birthday(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await callback_query.message.delete()
    await set_birthday(callback_query.message, locale=locale)