from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lang.messages import MESSAGES

def main_menu_keyboard(locale="ru"):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text=MESSAGES[locale]['back'], callback_data="main_menu"),
    )