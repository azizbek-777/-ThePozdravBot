from aiogram.dispatcher.filters.state import State, StatesGroup

class StateSendForward(StatesGroup):
    getMsg = State()