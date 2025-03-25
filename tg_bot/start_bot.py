import asyncio
from aiogram_dialog import setup_dialogs
from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeDefault

from create_bot import bot
from create_bot import dp
from tg_bot.handlers import router
from tg_bot.windows import dialog


async def set_commands():
    commands = [
        BotCommand(command="start", description="Старт"),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    dp.include_routers(
        router,
        dialog,
    )
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands()
    await dp.run_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())