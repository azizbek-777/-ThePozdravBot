from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters import Text

from keyboards.inline import generate_days_keyboard
from loader import dp
import calendar


DATA_PHRASE = [
    'daynav_prev_month',
    'daynav_next_month'
]

@dp.callback_query_handler(Text(startswith=DATA_PHRASE))
async def process_month_navigation(callback_query: CallbackQuery):    
    _, year, month = callback_query.data.split(":")
    year = int(year) 
    month = int(month)  

    if callback_query.data.startswith("daynav_prev_month"):
        new_month = month - 1
    elif callback_query.data.startswith("daynav_next_month"):
        new_month = month + 1
    
    if new_month < 1:
        new_month = 12
        year -= 1 
    elif new_month > 12:
        new_month = 1
        year += 1  
        
    await callback_query.answer(f"{year}, {calendar.month_name[new_month]}")
    
    keyboard = generate_days_keyboard(year, new_month)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
