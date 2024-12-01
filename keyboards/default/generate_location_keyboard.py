from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def generate_location_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(text="Отправить локацию", request_location=True),
        KeyboardButton(text="Не хочу")
    ]
    keyboard.add(*buttons)
    return keyboard