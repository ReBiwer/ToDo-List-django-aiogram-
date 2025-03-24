import os

import dotenv
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

dotenv.load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_NUM_DB = os.environ.get("REDIS_NUM_DB")

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_NUM_DB}"

bot = Bot(
    token=os.environ.get("BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
storage = RedisStorage.from_url(redis_url)
dp = Dispatcher(storage=storage)