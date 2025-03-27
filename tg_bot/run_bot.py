import dotenv
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_dialog import setup_dialogs
from windows import start_router, start_dialog, create_dialog, change_dialog

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


storage = MemoryStorage()
bot = Bot(token=os.environ.get("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher(storage=storage)
dp.include_router(change_dialog)
dp.include_router(start_dialog)
dp.include_router(create_dialog)
dp.include_router(start_router)
setup_dialogs(dp)


if __name__ == '__main__':
    dp.run_polling(bot, skip_updates=True)