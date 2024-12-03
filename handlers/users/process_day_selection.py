import calendar
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext


from keyboards.inline import generate_confirmation_keyboard
from lang.messages import MESSAGES
from loader import dp

@dp.callback_query_handler(text_contains="day")
async def process_day_selection(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await callback_query.answer()
    _, year, month, day = callback_query.data.split(":")
    day, month, year = int(day), int(month), int(year)

    await callback_query.message.edit_text(
        MESSAGES[locale]["birthday_confirmation"].format(f"{day:02d}", calendar.month_name[month], year),
        reply_markup=generate_confirmation_keyboard(day, month, year, locale)
    )