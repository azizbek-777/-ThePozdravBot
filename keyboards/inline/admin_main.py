from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_main_btn(): 
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(text="Отправить сообщение", callback_data="send_message")
    ).add(
        InlineKeyboardButton(text="Отправить сообщение(Forward)", callback_data="send_message_forward")
    )