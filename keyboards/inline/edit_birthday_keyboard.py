from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lang.messages import MESSAGES

def edit_birthday_keyboard(locale):
    keyboard = InlineKeyboardMarkup()
    add_group_button = InlineKeyboardButton(text=MESSAGES[locale]['edit'], 
                                            callback_data=f"edit_birthday")
    keyboard.add(add_group_button)
    keyboard.add(
        InlineKeyboardButton(text=MESSAGES[locale]['back'], callback_data="main_menu"),
    )
    return keyboard