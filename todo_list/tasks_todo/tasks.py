import asyncio

from aiogram import Bot
from celery import shared_task

from todo_list.settings import TELEGRAM_BOT_TOKEN


@shared_task(name="Уведомление о выполнении задачи")
def notification_start_task(msg: str, tg_id: int):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    asyncio.run(bot.send_message(tg_id, msg))
