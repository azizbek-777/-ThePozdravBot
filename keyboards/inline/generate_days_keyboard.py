from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import calendar

def generate_days_keyboard(year: int, month: int):
    days_in_month = calendar.monthrange(year, month)[1]
    
    keyboard = InlineKeyboardMarkup(row_width=6)

    navigation_buttons = [
        InlineKeyboardButton(text="⬅️", callback_data=f"daynav_prev_month:{year}:{month}"),
        InlineKeyboardButton(text=f"{year}, {calendar.month_name[month]}", callback_data=f"current_month:{year}:{month}"),
        InlineKeyboardButton(text="➡️", callback_data=f"daynav_next_month:{year}:{month}")
    ]
    keyboard.row(*navigation_buttons)

    day_buttons = [
        InlineKeyboardButton(text=str(day), callback_data=f"day:{year}:{month}:{day}")
        for day in range(1, days_in_month + 1)
    ]
    keyboard.add(*day_buttons)

    return keyboard
