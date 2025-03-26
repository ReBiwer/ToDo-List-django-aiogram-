import dotenv
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from aiogram_dialog import setup_dialogs
from routers.start import start_router, start_dialog

dotenv.load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_NUM_DB = os.environ.get("REDIS_NUM_DB_TG")

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_NUM_DB}"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


storage = RedisStorage.from_url(redis_url)
bot = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(storage=storage)
dp.include_router(start_dialog)
dp.include_router(start_router)
setup_dialogs(dp)


if __name__ == '__main__':
    dp.run_polling(bot, skip_updates=True)