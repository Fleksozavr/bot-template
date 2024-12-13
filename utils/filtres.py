from database import requests as rq

from aiogram.filters import BaseFilter
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession


class IsAdmin(BaseFilter): 
    """Проверка на админа"""
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        return message.from_user.id in await rq.admin_ids(session=session)
    

class IsBanned(BaseFilter):
    """Проверка пользователя на блокировку в боте"""
    async def __call__(self, message: Message, session:AsyncSession) -> Message:
        user = await rq.user(tg_id=message.from_user.id, session=session)
        if user.is_banned:
            await message.answer('Вы заблокированы, и не можете пользоватся ботом.')
            return False
        else:
            return True