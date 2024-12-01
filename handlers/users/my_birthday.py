from aiogram import types
from keyboards.inline import edit_birthday_keyboard

from loader import dp, db
from utils.misc import send_birthday_message, set_birthday

@dp.message_handler(commands=["my_birthday"])
async def handle_birthday_command(message: types.Message):
    chat_type = message.chat.type
    user_id = message.from_user.id
    
    birthday = await db.get_user_birthday(user_id)
    
    if not birthday:
        if chat_type in ["group", "supergroup"]:
            bot = await dp.bot.get_me()
            await send_birthday_message(message, bot.username)
        elif chat_type == "private":
            await set_birthday(message)
        return
    
    if chat_type == "private":
        text = f"Ваш день рождения: {birthday}"
        await message.answer(text, reply_markup=edit_birthday_keyboard())
    
    if chat_type in ["group", "supergroup"]:
        text = f"Ваш день рождения: {birthday}"
        await message.reply(text)
