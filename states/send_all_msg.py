from aiogram.dispatcher.filters.state import State, StatesGroup

class StateSendMessage(StatesGroup):
    getMsg = State()