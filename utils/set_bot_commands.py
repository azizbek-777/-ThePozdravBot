from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
            types.BotCommand("help", "керек"),
            types.BotCommand("my_birthday", "my birthday"),
            types.BotCommand("language", "язык"),
        ]
    )
