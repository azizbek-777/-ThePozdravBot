from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards.inline import generate_days_keyboard
from lang.messages import MESSAGES
from loader import dp

@dp.callback_query_handler(text_contains="month")
async def process_month_selection(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await callback_query.answer()
    _, month, year = callback_query.data.split(":")
    await callback_query.message.edit_text(MESSAGES[locale]["select_birth_day"], 
                                           reply_markup=generate_days_keyboard(int(year), int(month)))
