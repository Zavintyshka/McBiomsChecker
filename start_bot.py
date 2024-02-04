from asyncio import run
from aiogram import Dispatcher
from bot_initialize import bot
from logger import bot_logger
from core.handlers import *
from core.fsm import *
from core.middlewares import *


async def start_bot():
    msg = 'Bot started'
    bot_logger.debug(msg)


async def shutdown():
    msg = f'Bot shutdown'
    bot_logger.debug(msg)


dp = Dispatcher()
dp.startup.register(start_bot)
dp.shutdown.register(shutdown)

dp.message.middleware.register(LanguageMiddleware())

registrate_admin_fsm_handlers(dp)
registrate_user_fsm_handlers(dp)
registrate_message_handlers(dp)
registrate_callback_handlers(dp)


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(start())
