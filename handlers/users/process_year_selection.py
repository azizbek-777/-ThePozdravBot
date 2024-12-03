from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards.inline import generate_months_keyboard
from lang.messages import MESSAGES
from loader import dp

@dp.callback_query_handler(text_contains="year")
async def process_year_selection(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await callback_query.answer()
    year = callback_query.data.split(":")[1]
    text = MESSAGES[locale]["select_birth_month"]
    await callback_query.message.edit_text(text, reply_markup=generate_months_keyboard(int(year), locale))   