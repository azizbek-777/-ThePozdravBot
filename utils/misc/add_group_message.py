from aiogram.types import Message

from keyboards.inline import add_group_keyboard

async def add_group_message(message: Message, dp):
    bot = await dp.bot.get_me()
    text = "Добавьте меня в группу, чтобы я мог напоминать о днях рождениях! Просто нажмите на кнопку ниже, чтобы добавить меня в группу."
    await message.answer(
        text,
        reply_markup=add_group_keyboard(bot.username)
    )