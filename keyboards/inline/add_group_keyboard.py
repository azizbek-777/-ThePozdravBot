from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def add_group_keyboard(bot_username: str):
    keyboard = InlineKeyboardMarkup()
    
    add_group_button = InlineKeyboardButton(text="Добавить в группу ", 
                                            url=f"https://t.me/{bot_username}?startgroup=pm")
    keyboard.add(add_group_button)
    
    return keyboard