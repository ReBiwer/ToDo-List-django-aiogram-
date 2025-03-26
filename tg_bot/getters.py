from typing import Dict, Any

from aiogram_dialog import DialogManager


async def getter_tasks_list(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    tasks = dialog_manager.start_data["tasks"]
    return {"tasks": tasks}
