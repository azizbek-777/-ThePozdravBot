from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from keyboards.inline import generate_months_keyboard
from loader import dp

DATA_PHRASE = [
    'prev_year_from_month',
    'next_year_from_month'
]

@dp.callback_query_handler(Text(startswith=DATA_PHRASE))
async def process_year_navigation(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    
    current_year = int(callback_query.data.split(":")[1])
    new_year = current_year - 1 if callback_query.data.startswith("prev_year") else current_year + 1
    await callback_query.answer(new_year)
    
    keyboard = generate_months_keyboard(new_year, locale)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)