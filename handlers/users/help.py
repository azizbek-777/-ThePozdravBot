from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp

@dp.message_handler(CommandHelp(), chat_type="private")
async def bot_help(message: Message):
    text = "/language - Изменение языка бота" \
    "/my_birthday - Изменить ili Добавить день рождения\n"
    await message.reply(text)