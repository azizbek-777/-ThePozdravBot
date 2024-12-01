from aiogram.types import CallbackQuery
from keyboards.inline import generate_months_keyboard

from loader import dp

@dp.callback_query_handler(text_contains="year")
async def process_year_selection(callback_query: CallbackQuery):
    await callback_query.answer()
    year = callback_query.data.split(":")[1]
    text = "Отлично! Теперь выберите месяц вашего рождения:"
    await callback_query.message.edit_text(text, reply_markup=generate_months_keyboard(int(year)))   