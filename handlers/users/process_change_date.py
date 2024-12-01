from aiogram.types import CallbackQuery

from keyboards.inline import generate_years_keyboard
from loader import dp

@dp.callback_query_handler(text_contains="change_date")
async def process_change_date(callback_query: CallbackQuery):
    await callback_query.answer()
    text = "Выберите год вашего рождения:"
    await callback_query.message.edit_text(text, reply_markup=generate_years_keyboard(2001)) 