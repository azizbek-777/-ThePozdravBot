from aiogram.types import Message

from keyboards.inline import my_groups_keyboard
from loader import dp, db

@dp.message_handler(commands=['my_groups'], chat_type="private")
async def bot_my_groups(message: Message):
    text = "Выберите группу, которую вы хотите настроить."
    groups = await db.my_reminder_groups(message.from_user.id)
    print(groups)
    keyboard = await my_groups_keyboard(groups, dp)
    await message.reply(text, reply_markup=keyboard)