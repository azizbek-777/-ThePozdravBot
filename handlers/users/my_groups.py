from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.inline import my_groups_keyboard
from lang.messages import MESSAGES
from loader import dp, db

@dp.message_handler(commands=['my_groups'], chat_type="private")
async def bot_my_groups(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    text = MESSAGES[locale]["select_group"]
    groups = await db.my_reminder_groups(message.from_user.id)
    keyboard = await my_groups_keyboard(groups, dp, locale)
    await message.reply(text, reply_markup=keyboard)