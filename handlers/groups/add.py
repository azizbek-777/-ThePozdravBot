from aiogram.types import Message

from loader import dp
from keyboards.inline import add_birthday_keyboard

@dp.message_handler(commands=['add'], chat_type="group")
async def bot_add_group(message: Message):
    text = "Нажмите эту кнопку 👇, чтобы добавить свой день рождения."
    bot = await dp.bot.get_me()
    await message.reply(text, reply_markup=add_birthday_keyboard(bot.username, message.chat.id))
