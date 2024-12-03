from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from utils.misc import send_birthday_message

@dp.message_handler(content_types=["new_chat_members"])
async def bot_new_chat_member(message: types.Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    for new_member in message.new_chat_members:
        bot = await dp.bot.get_me()
        if new_member.id == bot.id:
            try:
                await send_birthday_message(message, bot.username, locale)
                await db.add_group(message.chat.id)
                break
            except Exception as err:
                print(err)
                break
