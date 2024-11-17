from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple

def subscription_btn(data: List[Tuple[str, str]]) -> InlineKeyboardMarkup:
    buttons = []
    for channel_name, channel_link in data:
        buttons.append(InlineKeyboardButton(text=channel_name, url=channel_link))
    
    # Tekshirish tugmachasini qo'shamiz
    buttons.append(InlineKeyboardButton(text="✅Tekseriw", callback_data='check_subs'))
    
    return InlineKeyboardMarkup(row_width=1).add(*buttons)


