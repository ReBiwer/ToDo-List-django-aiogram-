from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog

from aiogram.filters.state import State, StatesGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format
from tg_bot import utils
from tg_bot.getters import getter_tasks_list


class MainStates(StatesGroup):
    START = State()
    LIST = State()


start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainStates.START, mode=StartMode.RESET_STACK)


async def get_task_list(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    result = await utils.fetch_all_tasks(2147483647)
    tasks = utils.convert_list_tasks(result)
    await dialog_manager.start(MainStates.LIST, data={"tasks": tasks})



start_window = Window(
    Const("Добро пожаловать в ToDo-List"),
    Button(Const("Показать задачи"), id="list_tasks", on_click=get_task_list),
    Button(Const("Добавить задачу"), id="create_task"),
    state=MainStates.START,
)

list_window = Window(
    Const("Список ваших задач"),
    Select(
        Format("{item[title]}"),
        id="select_task",
        item_id_getter=lambda item: item["pk_task"],
        items="tasks"
    ),
    getter=getter_tasks_list,
    state=MainStates.LIST
)

start_dialog = Dialog(start_window, list_window)