from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lang.messages import MESSAGES

def add_group_keyboard(bot_username: str, locale):
    keyboard = InlineKeyboardMarkup()
    
    add_group_button = InlineKeyboardButton(text=MESSAGES[locale]['add_to_group'], 
                                            url=f"https://t.me/{bot_username}?startgroup=pm")
    keyboard.add(add_group_button)
    
    return keyboard