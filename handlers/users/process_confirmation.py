from aiogram.types import CallbackQuery
from keyboards.default import generate_location_keyboard
from loader import dp, db
from datetime import datetime

@dp.callback_query_handler(text_contains="confirm")
async def process_confirmation(callback_query: CallbackQuery):
    _, year, month, day = callback_query.data.split(":")
    await callback_query.answer()
    
    birthday = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date()
    await db.set_user_birthdate(birthday, callback_query.from_user.id)
    
    text = "Спасибо! Ваш день рождения записан!"
    await callback_query.message.edit_text(text) 
    
    text = "🌍 Теперь отправьте, пожалуйста, свою геолокацию, чтобы я мог правильно определить вашу таймзону"
    await callback_query.message.answer(text, reply_markup=generate_location_keyboard())
