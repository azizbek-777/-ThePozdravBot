from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup

from keyboards.inline import add_birthday_keyboard

def generate_birthday_message(bot_username: str, chat_id: int, locale) -> tuple[str, ReplyKeyboardMarkup]:
    """
    Generates a birthday message and reply markup.

    :param bot_username: The username of the bot.
    :return: A tuple containing the message text and reply markup.
    """
    text = (
        "Привет всем! Спасибо, что добавили меня в свою группу! 🎉 "
        "Я помогу вашей группе всегда помнить о днях рождениях!\n\n"
        "Нажмите кнопку ниже, чтобы добавить ваш день рождения в календарь группы\n\n"
        "Чтобы посмотреть другие настройки, отправьте /help"
    )

    # Replace this with your actual reply markup generation logic
    reply_markup = add_birthday_keyboard(bot_username, chat_id, locale)
    return text, reply_markup


async def send_birthday_message(message: Message, bot_username: str, locale):
    """
    Sends the birthday message to the user.

    :param message: The incoming message object.
    :param bot_username: The username of the bot.
    """
    text, reply_markup = generate_birthday_message(bot_username, message.chat.id)
    await message.answer(text, reply_markup=reply_markup)