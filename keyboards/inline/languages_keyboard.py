from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def languages_keyboard(method_type):
    language = {
        "Русский": "ru",
        "O'zbekcha": "uz",
        "Qaraqalpaqsha": "ka"
    }
    keyboard = InlineKeyboardMarkup()
    for language_name, language_code in language.items():
        keyboard.add(InlineKeyboardButton(text=language_name, callback_data=f"language:{language_code}:{method_type}"))
    return keyboard
