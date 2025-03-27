import utils
from datetime import datetime, date

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode, Dialog

from aiogram.filters.state import State, StatesGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Select, Next, Calendar, Back, Row
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format
from getters import getter_tasks_list, getter_task_info, getter_start


class MainStates(StatesGroup):
    START = State()
    LIST = State()
    INFO_TASK = State()


class CreateTask(StatesGroup):
    TITLE = State()
    DESCRIPTION = State()
    TAGS = State()
    DATE_END = State()


class ChangeTask(StatesGroup):
    TITLE = State()
    DESCRIPTION = State()
    TAGS = State()
    DATE_END = State()


start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainStates.START, mode=StartMode.RESET_STACK)


async def get_task_list(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    result = await utils.get_all_tasks(callback.from_user.id)
    tasks = utils.convert_list_tasks(result)
    await dialog_manager.start(MainStates.LIST, data={"tasks": tasks})


async def create_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(CreateTask.TITLE, mode=StartMode.RESET_STACK)


async def collect_info_new_task(callback: CallbackQuery, widget: Calendar,
                                dialog_manager: DialogManager, selected_date: date):
    title = dialog_manager.find("task_title").get_value()
    description = dialog_manager.find("task_description").get_value()
    tags: str = dialog_manager.find("task_tags").get_value()
    convert_date = datetime.combine(selected_date, datetime.time(datetime.now()))
    data = {
        "tg_id": callback.from_user.id,
        "title": title,
        "description": description,
        "tags": [
            {"name": tag}
            for tag in tags.split(', ')
        ],
        "date_end": str(convert_date)
    }
    await utils.create_new_task(data)
    await dialog_manager.start(MainStates.START, mode=StartMode.RESET_STACK, data={"created": True})


async def get_info_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):
    result = await utils.get_info_task(item_id)
    task_data = utils.convert_info_task(result)
    await dialog_manager.start(MainStates.INFO_TASK, data={"info_task": task_data})


async def change_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    pk_task = dialog_manager.start_data["info_task"]["pk_task"]
    await dialog_manager.start(ChangeTask.TITLE, mode=StartMode.RESET_STACK, data={"pk_task": pk_task})


async def collect_data_for_change_task(callback: CallbackQuery, widget: Calendar,
                      dialog_manager: DialogManager, selected_date: date):
    pk_task = dialog_manager.start_data["pk_task"]
    title = dialog_manager.find("task_title").get_value()
    description = dialog_manager.find("task_description").get_value()
    tags: str = dialog_manager.find("task_tags").get_value()
    convert_date = datetime.combine(selected_date, datetime.time(datetime.now()))
    data = {
        "tg_id": callback.from_user.id,
        "title": title,
        "description": description,
        "tags": [
            {"name": tag}
            for tag in tags.split(', ')
        ],
        "date_end": str(convert_date)
    }
    await utils.change_task(data, pk_task)
    await dialog_manager.start(MainStates.START, mode=StartMode.RESET_STACK, data={"changed": True})


async def delete_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    task_id = dialog_manager.start_data["info_task"]["pk_task"]
    await utils.delete_task(task_id)
    await dialog_manager.start(MainStates.START, data={"deleted": True})


start_window = Window(
    Const("Задача удалена!", when="deleted"),
    Const("Задача создана!", when="created"),
    Const("Задача изменена!", when="changed"),
    Const("Добро пожаловать в ToDo-List"),
    Button(Const("Показать задачи"), id="list_tasks", on_click=get_task_list),
    Button(Const("Добавить задачу"), id="create_task", on_click=create_task),
    state=MainStates.START,
    getter=getter_start,
)

create_dialog = Dialog(
    Window(
        Const("Введите заголовок задачи"),
        TextInput(id="task_title", on_success=Next()),
        Back(Const("Назад")),
        state=CreateTask.TITLE,
    ),
    Window(
        Const("Введите описание задачи"),
        TextInput(id="task_description", on_success=Next()),
        state=CreateTask.DESCRIPTION,
    ),
    Window(
        Const("Введите теги"),
        TextInput(id="task_tags", on_success=Next()),
        state=CreateTask.TAGS,
    ),
    Window(
        Const("Укажите дату наступления задачи"),
        Calendar(id="task_date_end", on_click=collect_info_new_task),
        state=CreateTask.DATE_END,
    )
)

change_dialog = Dialog(
    Window(
        Const("Введите новый заголовок задачи"),
        TextInput(id="task_title", on_success=Next()),
        Back(Const("Назад")),
        state=ChangeTask.TITLE,
    ),
    Window(
        Const("Введите новый описание задачи"),
        TextInput(id="task_description", on_success=Next()),
        state=ChangeTask.DESCRIPTION,
    ),
    Window(
        Const("Введите новые теги"),
        TextInput(id="task_tags", on_success=Next()),
        state=ChangeTask.TAGS,
    ),
    Window(
        Const("Укажите новую дату наступления задачи"),
        Calendar(id="task_date_end", on_click=collect_data_for_change_task),
        state=ChangeTask.DATE_END,
    )
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
    Back(Const("Назад")),
    getter=getter_tasks_list,
    state=MainStates.LIST
)

info_window = Window(
    Format("{title}\n"
           "Создана: {created_at}\n\n"
           "Описание: {description}\n"
           "Дата выполнения: {date_end}\n\n"
           "Теги: {tags}"),
    Row(Button(Const("Удалить"), id="delete_btn", on_click=delete_task),
         Button(Const("Изменить"), id="change_btn", on_click=change_task)
        ),
    Back(Const("Назад")),
    state=MainStates.INFO_TASK,
    getter=getter_task_info,
)

start_dialog = Dialog(start_window, list_window, info_window)