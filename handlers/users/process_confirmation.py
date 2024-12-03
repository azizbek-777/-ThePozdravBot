from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from keyboards.default import generate_location_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from datetime import datetime

@dp.callback_query_handler(text_contains="confirm")
async def process_confirmation(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    _, year, month, day = callback_query.data.split(":")
    await callback_query.answer()
    
    birthday = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date()
    await db.set_user_birthdate(birthday, callback_query.from_user.id)
    
    text = MESSAGES[locale]["birthday_saved"]
    await callback_query.message.edit_text(text) 
    
    text = MESSAGES[locale]["send_location"]
    await callback_query.message.answer(text, reply_markup=generate_location_keyboard(locale))
