from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.types import Message

from database.models import User, Admin

from logging import Logger


# Admin

async def admin_ids(session: AsyncSession):
    "Возвращает список с телеграм айди админов"
    result = await session.scalars(select(Admin.tg_id))

    return result.all()


async def set_admin(tg_id: int, session: AsyncSession, logger: Logger):
    """Добавляет администратора по Telegram ID."""
    try:
        new_admin = Admin(tg_id=tg_id)

        await session.execute(insert(Admin).values(tg_id=new_admin.tg_id))
        await session.commit()

        logger.info(f"Администратор с tg id {tg_id} добавлен")

        return True

    except IntegrityError as e:
        return False
    
    except Exception as e:
        logger.error(f"Ошибка при добавлении администратора: {e}")

        return False


#User

async def user(tg_id, session: AsyncSession, logger: Logger):
    """Получает обьект юзера"""
    try:
        result =  await session.scalar(select(User).where(User.tg_id == tg_id))

        return result
    except Exception as e:
        logger.error('Ошибка при попытке получения обьекта пользователя', e)

        return None


async def set_user(message: Message, session: AsyncSession, logger: Logger):
    """Добавляет пользователя в базу данных."""
    user = await session.scalar(select(User).where(User.tg_id == message.from_user.id))

    if not user:
        tg = message.from_user
        username = tg.username if tg.username else ""
 
        result = await session.execute(
            insert(User).values(
                tg_id=tg.id,
                username=username,
                full_name=tg.full_name
            )
        )
        await session.commit()

        new_user_id = result.inserted_primary_key[0]
        new_user = await session.scalar(select(User).where(User.id == new_user_id))


        logger.info(f"Пользователь с tg id {new_user.tg_id} добавлен")

        return new_user
    
    else:
        logger.error(f"Пользователь {user.tg_id} уже существует.")

        return user


async def unban_user(tg_id: int, session: AsyncSession):
    """Разбанит пользователя по Telegram ID."""
    try:
        user = await session.get(User, tg_id)
        if user:
            user.is_banned = False

            await session.commit()

            return True
        return False
    except Exception as e:

        await session.rollback()
        return False


async def ban_user(tg_id: int, session: AsyncSession):
    """Банит пользователя по Telegram ID."""
    try:
        user = await session.get(User, tg_id)
        if user:
            user.is_banned = True

            await session.commit()

            return True
        
        return False
    except Exception as e:
        await session.rollback()

        return False