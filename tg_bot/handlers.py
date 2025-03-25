from tkinter import Button

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from tg_bot.states import MainState

router = Router()

@router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainState.START, mode=StartMode.RESET_STACK)


async def get_list(callback: CallbackQuery, button: Button,
                     manager: DialogManager):
    pass

async def create_task(callback: CallbackQuery, button: Button,
                     manager: DialogManager):
    pass
