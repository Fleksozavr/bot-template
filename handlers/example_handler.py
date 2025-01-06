import os

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from sqlalchemy.ext.asyncio import AsyncSession

from database import requests as rq
from keyboards import reply, inline
from logging import Logger

from dotenv import load_dotenv


load_dotenv()
router = Router()


#Пример с ReplyKeyboardMarkup клавиатурой
@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, logger: Logger):
    user_id = message.from_user.id
    try:
        user = await rq.user(tg_id=user_id, session=session)
        if user:
            await message.answer(
                text="👋 Привет",
                reply_markup=await reply.main_keyboard(message.from_user.id, session, logger)
            )
            return

        else:
            await rq.set_user(message, session, logger)

        user = await rq.user(tg_id=user_id, session=session)
        if user:
            await message.answer(
                text="👋 Привет",
                reply_markup=await reply.main_keyboard(message.from_user.id, session, logger)
            )

    except Exception as e:
        logger.error(f"Error processing command: {e}")


#Пример с InlineKeyboardMarkup клавиатурой
@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, logger: Logger):
    user_id = message.from_user.id
    try:
        user = await rq.user(tg_id=user_id, session=session)
        if user:
            await message.answer(
                text="👋 Привет",
                reply_markup=await inline.main_keyboard(message.from_user.id, session, logger)
            )
            return

        else:
            await rq.set_user(message, session, logger)

        user = await rq.user(tg_id=user_id, session=session)
        if user:
            await message.answer(
                text="👋 Привет",
                reply_markup=await inline.main_keyboard(message.from_user.id, session, logger)
            )

    except Exception as e:
        logger.error(f"Error processing command: {e}")
