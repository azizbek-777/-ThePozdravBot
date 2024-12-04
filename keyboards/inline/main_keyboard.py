from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lang.messages import MESSAGES

def main_btn(bot_username, locale="ru"):
     
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=MESSAGES[locale]['add_to_group'], 
                                            url=f"https://t.me/{bot_username}?startgroup=pm")
    ).add(
        InlineKeyboardButton(text=MESSAGES[locale]['my_groups'], callback_data="my_groups"),
        InlineKeyboardButton(text=MESSAGES[locale]['my_birthday'], callback_data="my_birthday"),
    )