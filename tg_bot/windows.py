from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from tg_bot.handlers import get_list, create_task
from tg_bot.states import MainState

start_window = Window(
    Const("Добро пожаловать в ToDo list."),
    Row(
        Button(Const("Мои задачи"), id="get_list", on_click=get_list),
        Button(Const("Добавить задачу"), id="create_task", on_click=create_task),
    ),
    state=MainState.START
)

dialog = Dialog(start_window)
