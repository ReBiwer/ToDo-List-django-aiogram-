import asyncio
import logging
import os

import dotenv
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from routers import main_router

dotenv.load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_NUM_DB = os.environ.get("REDIS_NUM_DB_TG")

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_NUM_DB}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

bot = Bot(
    token=os.environ.get("TELEGRAM_BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
storage = RedisStorage.from_url(redis_url)
dp = Dispatcher(storage=storage)

async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    dp.include_router(main_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

