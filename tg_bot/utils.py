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
