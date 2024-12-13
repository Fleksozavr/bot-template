from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
    )

from sqlalchemy.ext.asyncio import AsyncSession
from database import requests as rq

from logging import Logger


async def main_keyboard(user_id: int, session: AsyncSession, logger: Logger) -> InlineKeyboardMarkup:
    user = await rq.user(user_id, session, logger)
    admin_ids = await rq.admin_ids(session)

    if user is None:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Вы не зарегистрированы!", callback_data="not_registered")]
            ]
        )
        return keyboard

    elif user.tg_id in admin_ids:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Админ кнопка", callback_data="admin_button")]
            ]
        )
        return keyboard

    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Просто кнопка", callback_data="simple_button")]
            ]
        )
        return keyboard