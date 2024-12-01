from aiogram import types
from keyboards.inline import languages_keyboard

from loader import dp, db
from utils.misc import send_congratulation_message

@dp.message_handler(commands=["language"])
async def bot_language(message: types.Message):
    await send_congratulation_message(dp, db)
    text = "🌍 Выберите язык, на котором хотите использовать бота:"
    await message.answer(text, reply_markup=languages_keyboard('update')) 
    
