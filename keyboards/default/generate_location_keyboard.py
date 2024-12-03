from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lang.messages import MESSAGES

def generate_location_keyboard(locale):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(text=MESSAGES[locale]['send_location'], request_location=True),
        KeyboardButton(text=MESSAGES[locale]['dont_want'])
    ]
    keyboard.add(*buttons)
    return keyboard