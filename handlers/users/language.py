from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import languages_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from utils.misc import send_congratulation_message

@dp.message_handler(commands=["language"])
async def bot_language(message: types.Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    await send_congratulation_message(dp, db)
    text = MESSAGES[locale]["select_language"]
    await message.answer(text, reply_markup=languages_keyboard('update')) 
    
