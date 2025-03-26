from typing import Dict, Any

from aiogram_dialog import DialogManager


async def getter_start(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    if dialog_manager.start_data:
        return {"deleted": dialog_manager.start_data["deleted"]}
    return {}


async def getter_tasks_list(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    tasks = dialog_manager.start_data["tasks"]
    return {"tasks": tasks}

async def getter_task_info(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    info: dict = dialog_manager.start_data["info_task"]
    return info
