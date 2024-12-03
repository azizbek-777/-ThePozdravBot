from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from lang.messages import MESSAGES
from loader import dp
from keyboards.inline import add_birthday_keyboard

@dp.message_handler(commands=['add'], chat_type="group")
async def bot_add_group(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]["add_birthday_button"]
    bot = await dp.bot.get_me()
    await message.reply(text, reply_markup=add_birthday_keyboard(bot.username, message.chat.id, locale))
