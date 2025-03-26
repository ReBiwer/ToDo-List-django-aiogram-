from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog

from aiogram.filters.state import State, StatesGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format
from tg_bot import utils
from tg_bot.getters import getter_tasks_list, getter_task_info


class MainStates(StatesGroup):
    START = State()
    LIST = State()
    INFO_TASK = State()


start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainStates.START, mode=StartMode.RESET_STACK)


async def get_task_list(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    result = await utils.fetch_all_tasks(1111)
    tasks = utils.convert_list_tasks(result)
    await dialog_manager.start(MainStates.LIST, data={"tasks": tasks})


async def get_info_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):
    result = await utils.get_info_task(item_id)
    task_data = utils.convert_info_task(result)
    await dialog_manager.start(MainStates.INFO_TASK, data={"info_task": task_data})


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
        items="tasks",
        on_click=get_info_task,
    ),
    getter=getter_tasks_list,
    state=MainStates.LIST
)

info_window = Window(
    Format("{title}\n"
           "Создана: {created_at}\n\n"
           "Описание: {description}\n"
           "Дата выполнения: {date_end}\n\n"
           "Теги: {tags}"),
    Button(Const("Удалить"), id="delete_btn"),
    Button(Const("Изменить"), id="change_btn"),
    state=MainStates.INFO_TASK,
    getter=getter_task_info,
)

start_dialog = Dialog(start_window, list_window, info_window)