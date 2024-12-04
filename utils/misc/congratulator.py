from aiogram import Dispatcher
from datetime import datetime
from pytz import timezone as pytz_timezone, UTC

# Normalize and handle timezone conversion
def normalize_timezone(user_timezone: str):
    if user_timezone.startswith(('+', '-')):
        try:
            hours_offset = int(user_timezone)
            return UTC if hours_offset == 0 else pytz_timezone(f"Etc/GMT{'+' if hours_offset < 0 else '-'}{abs(hours_offset)}")
        except ValueError:
            raise ValueError(f"Invalid timezone format: {user_timezone}")
    return pytz_timezone(user_timezone)  # Assume it's a valid named timezone

russian_months = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]

# Function to format birthday in Russian style
def format_birthday(birthday: datetime):
    return f"{birthday.day} {russian_months[birthday.month - 1]}"

async def send_congratulation_message(dp: Dispatcher, db):
    try:
        # Fetch reminder data once
        data = await db.get_reminder_groups_with_users()
        
        for group_id, user_id, birthday, user_timezone in data:
            tz = normalize_timezone(user_timezone)
            now = datetime.now(tz)
            
            # Check if today is the user's birthday
            if birthday.day == now.day and birthday.month == now.month:
                user = await dp.bot.get_chat(user_id)
                username = user.username
                if not username:
                    username = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
                else:
                    username = f"@{username}"
                
                formatted_birthday = format_birthday(birthday)  # Format the birthday
                
                message = (
                    f"🥳 Сегодня, <b>{formatted_birthday}</b>, день рождения у {username}!\n\n"
                    "Давайте поздравим с этим замечательным днем! 🎉\n"
                    "Пожелаем счастья, крепкого здоровья, успехов и исполнения всех желаний.\n\n"
                )
                # Send message to group chat
                await dp.bot.send_message(chat_id=group_id, text=message)

                # Send personal birthday message
                message = (
                    f"🥳 Сегодня *{formatted_birthday}* — ваш день рождения!\n\n"
                    "Поздравляем вас с этим замечательным событием! 🎉\n"
                    "Желаем счастья, крепкого здоровья, успехов во всех начинаниях и исполнения самых заветных желаний.\n\n"
                    "Пусть этот день станет незабываемым! 🎁✨"
                )
                await dp.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown")

    except Exception as e:
        print(f"Error sending birthday messages: {e}")
