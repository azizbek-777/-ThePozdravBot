from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext

from lang.messages import MESSAGES
from loader import dp

@dp.message_handler(CommandHelp(), chat_type="group")
async def bot_help_group(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]["commands_list_in_group"]
    await message.reply(text)
