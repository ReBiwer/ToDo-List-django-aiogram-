from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer("Хай")
