from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import edit_birthday_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from utils.misc import set_birthday

@dp.message_handler(commands=["my_birthday"], chat_type="private")
async def handle_birthday_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    user_id = message.from_user.id
    
    birthday = await db.get_user_birthday(user_id)
    
    if not birthday:
        await set_birthday(message, locale=locale)
        return
    
    text = MESSAGES[locale]["your_birthday"].format(birthday)
    await message.answer(text, reply_markup=edit_birthday_keyboard(locale))
