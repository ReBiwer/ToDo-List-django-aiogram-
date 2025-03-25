from sre_parse import State

from aiogram.fsm.state import StatesGroup


class MainState(StatesGroup):
    START = State()
    CREATE = State()


class ChangeState(StatesGroup):
    TITLE = State()
    DESCRIPTION = State()
