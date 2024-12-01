from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def generate_confirmation_keyboard(day: int, month: int, year: int):
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(text="Да", callback_data=f"confirm:{year}:{month}:{day}"),
        InlineKeyboardButton(text="Нет изменить", callback_data="change_date")
    ]
    keyboard.add(*buttons)

    return keyboard