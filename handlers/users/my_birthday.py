from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import edit_birthday_keyboard
from lang.messages import MESSAGES
from loader import dp, db
from utils.misc import send_birthday_message, set_birthday

@dp.message_handler(commands=["my_birthday"])
async def handle_birthday_command(message: types.Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    chat_type = message.chat.type
    user_id = message.from_user.id
    
    birthday = await db.get_user_birthday(user_id)
    
    if not birthday:
        if chat_type in ["group", "supergroup"]:
            bot = await dp.bot.get_me()
            await send_birthday_message(message, bot.username, locale)
        elif chat_type == "private":
            await set_birthday(message, locale=locale)
        return
    
    text = MESSAGES[locale]["your_birthday"].format(birthday)
    if chat_type == "private":
        await message.answer(text, reply_markup=edit_birthday_keyboard(locale))
    
    if chat_type in ["group", "supergroup"]:
        await message.reply(text)
