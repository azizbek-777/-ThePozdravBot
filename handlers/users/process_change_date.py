from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards.inline import generate_years_keyboard
from lang.messages import MESSAGES
from loader import dp

@dp.callback_query_handler(text_contains="change_date")
async def process_change_date(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await callback_query.answer()
    text = MESSAGES[locale]["select_birth_year"]
    await callback_query.message.edit_text(text, reply_markup=generate_years_keyboard(2001)) 