from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "♻️ Перезапустить бот"),
            types.BotCommand('my_birthday', '🎉 Мой день рождения'),
            types.BotCommand('my_groups', '👥 Мои группы'),
            types.BotCommand('language', '🌍 Язык'),
            types.BotCommand('help', '📗 Помощь'),
        ], 
        scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "♻️ Перезапустить бот"),
            types.BotCommand('add', '➕ Добавить день рождения'),
            types.BotCommand('list_birthday', '🎉 Список дней рождения'),
            types.BotCommand('help', '📗 Помощь'),
        ], 
        scope=types.BotCommandScopeAllGroupChats()
    )
    
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "♻️ Перезапустить бот"),
            types.BotCommand('add', '➕ Добавить день рождения'),
            types.BotCommand('list_birthday', '🎉 Список дней рождения'),
            types.BotCommand('language', '🌍 Язык'),
            types.BotCommand('help', '📗 Помощь'),
        ], 
        scope=types.BotCommandScopeAllChatAdministrators()
    )
