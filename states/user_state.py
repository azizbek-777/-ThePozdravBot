from aiogram.dispatcher.filters.state import State, StatesGroup

class UserState(StatesGroup):
    locale = State()