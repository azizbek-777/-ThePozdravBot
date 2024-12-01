from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import base64


def add_birthday_keyboard(bot_username: str, chat_id: int):
    keyboard = InlineKeyboardMarkup()
    
    key = f"addbirthday:{chat_id}"
    encoded_data = base64.b64encode(key.encode('utf-8')).decode('utf-8')
    add_group_button = InlineKeyboardButton(text="➕ Добавить день рождения", 
                                            url=f"https://t.me/{bot_username}?start={encoded_data}")
    keyboard.add(add_group_button)
    
    return keyboard