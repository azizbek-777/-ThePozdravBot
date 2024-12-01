from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandHelp
from datetime import datetime

from loader import dp, db

russian_months = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]

@dp.message_handler(commands=["list_birthday"], chat_type="group")
async def list_birthday(message: Message):
    data = await db.get_reminder_groups_with_users_where_group_id(message.chat.id)
    
    text = "Список день рождения участников группы \n\n"
    i = 1
    for _, user_id, birthday, _ in data:
        user = await dp.bot.get_chat(user_id)

        date_obj = datetime.strptime(str(birthday), "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.month
        
        formatted_date = f"{day} {russian_months[month - 1]}"
        
        text += f"{i}. <a href='tg://user?id={user.id}'>{user.full_name}</a> - {formatted_date}\n"
        i += 1
        
    await message.reply(text)
