from aiogram.types import CallbackQuery
from keyboards.inline import generate_days_keyboard

from loader import dp

@dp.callback_query_handler(text_contains="month")
async def process_month_selection(callback_query: CallbackQuery):
    await callback_query.answer()
    _, month, year = callback_query.data.split(":")
    await callback_query.message.edit_text("Теперь выберите день вашего рождения:", 
                                           reply_markup=generate_days_keyboard(int(year), int(month)))
