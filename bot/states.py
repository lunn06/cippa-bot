from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    name = State()
    clear_name = State()
    city = State()
    clear_city = State()
    preschool = State()
    position = State()
    final = State()
