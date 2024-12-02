from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from datetime import datetime

from lang.messages import MESSAGES
from loader import dp, db

@dp.message_handler(commands=["list_birthday"], chat_type="group")
async def list_birthday(message: Message, state: FSMContext):
    data = await state.get_data()
    locale = data.get("locale", "ru")
    data = await db.get_reminder_groups_with_users_where_group_id(message.chat.id)
    
    text = MESSAGES[locale]["birthday_list_group"]
    i = 1
    for _, user_id, birthday, _ in data:
        user = await dp.bot.get_chat(user_id)

        date_obj = datetime.strptime(str(birthday), "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.month
        
        formatted_date = f"{day} {MESSAGES[locale]['months'][month - 1]}"
        
        text += MESSAGES[locale]["birthday_list_item"].format(user.id, user.full_name, formatted_date)
        i += 1
        
    await message.reply(text)
