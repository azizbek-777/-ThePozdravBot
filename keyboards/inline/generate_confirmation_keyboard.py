from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lang.messages import MESSAGES

def generate_confirmation_keyboard(day: int, month: int, year: int, locale):
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(text=MESSAGES[locale]['yes'], callback_data=f"confirm:{year}:{month}:{day}"),
        InlineKeyboardButton(text=MESSAGES[locale]['no_edit'], callback_data="change_date")
    ]
    keyboard.add(*buttons)

    return keyboard