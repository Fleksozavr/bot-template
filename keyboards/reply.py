from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
    )

from sqlalchemy.ext.asyncio import AsyncSession
from database import requests as rq

from logging import Logger


async def main_keyboard(user_id: int, session: AsyncSession, logger: Logger) -> ReplyKeyboardMarkup:
    user = await rq.user(user_id, session, logger)
    admin_ids = await rq.admin_ids(session)

    if user is None:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Вы не зарегестрированы!")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        return keyboard

    elif user.tg_id in admin_ids:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Админ кнопка")],
            ],
            resize_keyboard=True
        )
        return keyboard

    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Просто кнопка")],
            ],
            resize_keyboard=True
        )
        return keyboard