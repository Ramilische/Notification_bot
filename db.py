from os import getenv
import dotenv
import tracemalloc
import asyncio

from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker

from models import Base, User, Profile, Website, Form

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


async def add_user(async_session: async_sessionmaker[AsyncSession], chat_id: int, username: str, first_name: str = None, last_name: str = None, is_admin: bool = False) -> None:
    new_user = User(chat_id=chat_id, is_admin=is_admin)
    new_profile = Profile(username=username, first_name=first_name, last_name=last_name, user=new_user)
    async with async_session() as session:
        async with session.begin():
            session.add_all([new_profile, new_user])


async def async_main(func: asyncio.coroutines, *args, **kwargs) -> None:
    settings = Settings()
    db_url = settings.get_db_url_pg()
    engine = create_async_engine(db_url, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    task = asyncio.create_task(func(async_session, *args, **kwargs))
    await task
    await engine.dispose()


if __name__ == '__main__':
    # Тест
    asyncio.run(async_main(add_user, 98709869, 'ramilische'))