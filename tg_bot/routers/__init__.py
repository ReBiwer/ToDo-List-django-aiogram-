from .start import start_router
from aiogram import Router

main_router = Router()
main_router.include_routers(start_router)
