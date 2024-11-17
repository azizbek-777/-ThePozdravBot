from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple

def nominations_btn(data: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
    buttons = []
    for name, nomination_id in data:
        buttons.append(InlineKeyboardButton(text=name, callback_data=f"nomination:{nomination_id}"))
    
    buttons.append(InlineKeyboardButton(text="📊 Reyting", callback_data="reyting"))
    return InlineKeyboardMarkup(row_width=1).add(*buttons)
