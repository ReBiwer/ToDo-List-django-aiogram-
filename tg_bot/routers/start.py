from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog

from aiogram.filters.state import State, StatesGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


class MainStates(StatesGroup):
    START = State()


start_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Useless button"), id="nothing"),
    state=MainStates.START,
)

start_dialog = Dialog(start_window)
start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainStates.START, mode=StartMode.RESET_STACK)
