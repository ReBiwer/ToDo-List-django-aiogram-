import json

import dotenv
import os
import aiohttp
from pydantic import with_config

dotenv.load_dotenv()

API_URL = os.environ.get("API_URL")

async def get_all_tasks(tg_id: int):
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
    tags = [tag["name"] for tag in result["tags"]]
    formated_tags = ', '.join(tags)
    return {
        "pk_task": result["pk_task"],
        "title": result["title"],
        "created_at": result["created_at"],
        "description": result["description"],
        "date_end": result["date_end"],
        "tags": formated_tags,
    }

async def delete_task(task_id: str):
    url = API_URL + f"tasks/{task_id}/"
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as response:
            return response.status

async def create_new_task(data: dict):
    url = API_URL + "tasks/"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
    }
    json_data = json.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            return await response.text()
