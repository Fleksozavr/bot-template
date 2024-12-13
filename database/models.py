import os

from sqlalchemy import BigInteger, String, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession

from dotenv import load_dotenv


load_dotenv()

engine = create_async_engine(url=os.getenv('DB_URL'))
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    def __repr__(self):
        return str(vars(self)) 


class Admin(Base):
    __tablename__ = 'admins'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))

    is_banned: Mapped[int] = mapped_column(Boolean, default=False)


async def create_db():
    async with AsyncSession(engine) as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)