from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def edit_birthday_keyboard():
    keyboard = InlineKeyboardMarkup()
    add_group_button = InlineKeyboardButton(text="Изменить", 
                                            callback_data=f"edit_birthday")
    keyboard.add(add_group_button)
    return keyboard