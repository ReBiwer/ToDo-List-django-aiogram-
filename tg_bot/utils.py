import dotenv
import os
import aiohttp

dotenv.load_dotenv()

API_URL = os.environ.get("API_URL")

async def fetch_all_tasks(tg_id: int):
    url = API_URL + f'tasks/?tg_id={tg_id}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

def convert_list_tasks(result: dict):
    tasks = []
    for task in result:
        task_info = {
            "title": task["title"],
            "pk_task": task["pk_task"]
        }
        tasks.append(task_info)
    return tasks

async def get_info_task(task_id: str):
    url = API_URL + f"tasks/{task_id}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

def convert_info_task(result: dict):
    formated_tags = ', '.join(result["tags"])
    return {
        "pk_task": result["pk_task"],
        "title": result["title"],
        "created_at": result["created_at"],
        "description": result["description"],
        "date_end": result["date_end"],
        "tags": formated_tags,
    }
