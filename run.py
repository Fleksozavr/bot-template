import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties

from utils.middlewares import LoggingMiddleware, DataBaseSession
from database.models import async_session, create_db
from handlers import example_handler


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

        
async def main():
    await create_db()

    dp.include_routers(example_handler.router)

    dp.update.middleware(DataBaseSession(session_pool=async_session))
    dp.update.middleware(LoggingMiddleware())

    await bot.delete_webhook(True)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass