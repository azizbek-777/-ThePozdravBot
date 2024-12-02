from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
            types.BotCommand("add", "Добавить свой день рождения"),   
            types.BotCommand("help", "керек"),
            types.BotCommand("my_birthday", "my birthday"),
            types.BotCommand("my_groups", "my groups"),
            types.BotCommand("language", "язык"),
        ]
    )
