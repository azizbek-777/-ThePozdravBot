from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text

from keyboards.inline import generate_years_keyboard
from loader import dp

START_YEAR = 2001
YEARS_PER_PAGE = 15

@dp.callback_query_handler(Text(startswith=["prev", "next"]))
async def process_pagination(callback_query: CallbackQuery):
    await callback_query.answer()
    current_start_year = int(callback_query.data.split(":")[1])
    if callback_query.data.startswith("prev"):
        new_start_year = current_start_year - YEARS_PER_PAGE
    else:
        new_start_year = current_start_year + YEARS_PER_PAGE
    
    keyboard = generate_years_keyboard(new_start_year)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)