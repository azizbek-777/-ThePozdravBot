from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def generate_years_keyboard(start_year: int = 2001):
    keyboard = InlineKeyboardMarkup(row_width=5)
    
    navigation_buttons = [
        InlineKeyboardButton(text="⬅️", callback_data=f"prev:{start_year}"),
        InlineKeyboardButton(text="➡️", callback_data=f"next:{start_year}")
    ]
    keyboard.row(*navigation_buttons)
    
    year_buttons = [
        InlineKeyboardButton(text=str(year), callback_data=f"year:{year}")
        for year in range(int(start_year), int(start_year) + 20)
    ]
    keyboard.add(*year_buttons)
    
    return keyboard
