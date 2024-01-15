import asyncio
from aiogram import Dispatcher
from logger import bot_logger
from core.handlers.message_handlers import register_handlers
from core.handlers.callback_handlers import register_callback_handlers
from core.user_fsm import register_fsm_handlers
from bot_initialize import bot
from core.admin_fsm import registrate_admin_fsm_handlers


async def start_bot():
    msg = 'Bot started'
    bot_logger.debug(msg)


async def shutdown():
    msg = f'Bot shutdown'
    bot_logger.debug(msg)


dp = Dispatcher()
dp.startup.register(start_bot)
dp.shutdown.register(shutdown)

# Handlers Registration
registrate_admin_fsm_handlers(dp)
register_fsm_handlers(dp)
register_handlers(dp)
register_callback_handlers(dp)


async def start():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())
