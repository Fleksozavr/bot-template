import logging

from logging.handlers import TimedRotatingFileHandler

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Dict, Any, Awaitable


class DataBaseSession(BaseMiddleware):
    """Создает асинхронную сессию базы данных"""
    def __init__(self, session_pool):
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    """Создает класс для обработки событий в боте"""
    def __init__(self):
        super().__init__()
        pattern = "%(asctime)s | %(levelname)s | %(filename)s -> %(funcName)s():%(lineno)s | %(message)s"
        logger = logging.getLogger("bot")
        logger.setLevel(logging.DEBUG)

        info_handler = TimedRotatingFileHandler(
            filename="logs/info.log",
            when="midnight",
            interval=1,
            backupCount=10,
            encoding="utf-8"
        )
        info_handler.setLevel(logging.INFO)
        info_handler.addFilter(lambda record: record.levelno == logging.INFO)
        info_handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter(pattern)
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)

        error_handler = TimedRotatingFileHandler(
            filename="logs/error.log",
            when='midnight',
            interval=1,
            backupCount=10,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        error_handler.suffix = "%Y-%m-%d"
        logger.addHandler(error_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
        self.logger = logger

    async def __call__(self, handler, event, data):
        data['logger'] = self.logger
        return await handler(event, data)