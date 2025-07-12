import asyncio

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from db_scripts.models import Base, User, Profile, Website, Form

#   CRUD для таблицы User


async def add_user(async_session: async_sessionmaker[AsyncSession], first_name=None, last_name=None, is_admin=False, **kwargs) -> None:
    """
        Добавление пользователя в базу. Все поля следует указывать явно
    """
    new_user = User(chat_id=kwargs['chat_id'], is_admin=is_admin)
    new_profile = Profile(
        username=kwargs['username'],
        first_name=first_name,
        last_name=last_name,
        user=new_user
    )
    async with async_session() as session:
        async with session.begin():
            session.add_all([new_profile, new_user])


async def get_user_by_id(async_session: async_sessionmaker[AsyncSession], chat_id: int):
    """
        Получение объекта типа User по ID чата
    :param async_session: сессия типа AsyncSession
    :param chat_id: ID чата пользователя с ботом
    """
    async with async_session() as session:
        async with session.begin():
            return await session.execute(select(User).filter(User.chat_id == chat_id))


async def get_user_by_username(async_session: async_sessionmaker[AsyncSession], username: str):
    """
        Получение объекта типа User по юзернейму профиля
    :param async_session: сессия типа AsyncSession
    :param username: юзернейм пользователя без символа @
    """
    async with async_session() as session:
        async with session.begin():
            return await session.execute(select(User).filter(User.profile.has(username=username)))


async def update_user(async_session: async_sessionmaker[AsyncSession], chat_id: int, **kwargs):
    """
        Обновление строк пользователя и профиля по ID чата. В kwargs хранятся измененные параметры
    :param async_session: сессия типа AsyncSession
    :param chat_id: ID чата пользователя с ботом
    :param kwargs: словарь параметров
    """
    res = await get_user_by_id(async_session, chat_id)
    user = res.scalars().all()[0]
    profile = user.profile
    for key, value in kwargs.items():
        if value is not None:
            if key in ('first_name', 'last_name', 'username'):
                setattr(profile, key, value)
            else:
                setattr(user, key, value)
    async with async_session() as session:
        async with session.begin():
            session.add_all([profile, user])


async def delete_user(async_session: async_sessionmaker[AsyncSession], chat_id: int):
    """
        Удаление пользователя и связанного с ним профиля по ID
    :param async_session: сессия типа AsyncSession
    :param chat_id: ID чата пользователя с ботом
    """
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Profile).filter(Profile.user.has(chat_id=chat_id)))
            await session.execute(delete(User).filter(User.chat_id == chat_id))
            return None
