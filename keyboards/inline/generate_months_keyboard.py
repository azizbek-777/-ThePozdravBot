from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lang.messages import MESSAGES

def generate_months_keyboard(year: int, locale):
    months = MESSAGES[locale]["months"]
    
    keyboard = InlineKeyboardMarkup(row_width=3)

    # Yil navigatsiya tugmalari
    navigation_buttons = [
        InlineKeyboardButton(text="⬅️", callback_data=f"prev_year_from_month:{year}"),
        InlineKeyboardButton(text=str(year), callback_data=f"current_year_from_month:{year}"),
        InlineKeyboardButton(text="➡️", callback_data=f"next_year_from_month:{year}"),
    ]
    keyboard.row(*navigation_buttons)

    # Oy tugmalari
    month_buttons = [
        InlineKeyboardButton(text=month, callback_data=f"month:{index + 1}:{year}")
        for index, month in enumerate(months)
    ]
    keyboard.add(*month_buttons)

    return keyboard
