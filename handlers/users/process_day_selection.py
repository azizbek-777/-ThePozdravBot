import calendar
from aiogram.types import CallbackQuery

from keyboards.inline import generate_confirmation_keyboard
from loader import dp

@dp.callback_query_handler(text_contains="day")
async def process_day_selection(callback_query: CallbackQuery):
    await callback_query.answer()
    _, year, month, day = callback_query.data.split(":")
    day, month, year = int(day), int(month), int(year)

    await callback_query.message.edit_text(
        f"Ваш день рождения: {day:02d} {calendar.month_name[month]} {year} года.\nПравильно?",
        reply_markup=generate_confirmation_keyboard(day, month, year)
    )