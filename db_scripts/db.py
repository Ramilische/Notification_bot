from os import getenv
import dotenv
import tracemalloc
import asyncio

from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker

from db_scripts.models import Base, User, Profile, Website, Form
from db_scripts.user import add_user, get_user_by_id, get_user_by_username

"""
    Здесь будет CRUD и подключение к БД
    Перешел на Postgres
"""


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file='.env/db.env')

    def get_db_url_pg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


async def async_main(func: asyncio.coroutines, *args, **kwargs):
    """
        Единая функция для CRUD
    :param func: функция, которую надо выполнить
    """
    settings = Settings()
    db_url = settings.get_db_url_pg()
    engine = create_async_engine(db_url, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(func(async_session, *args, **kwargs))
    await engine.dispose()
    if task.result() is None:
        return 0
    print(task.result())
    return task.result().scalars().all()


async def get_one(func: asyncio.coroutines, *args, **kwargs):
    """
        Получение данных с помощью функции func
    :param func: функция, которую надо выполнить
    """
    result = await async_main(func, *args, **kwargs)
    return result[0] if len(result) != 0 else None


async def get_many(func: asyncio.coroutines, *args, **kwargs) -> None:
    """
        Изменение данных с помощью функции func
    :param func: функция, которую надо выполнить
    """

    return await async_main(func, *args, **kwargs)


async def do(func: asyncio.coroutines, *args, **kwargs) -> None:
    """
        Изменение данных с помощью функции func
    :param func: функция, которую надо выполнить
    """
    await async_main(func, *args, **kwargs)