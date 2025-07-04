from os import getenv
import dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker

from models import Base, User


class Settings(BaseSettings):
    DB_PATH: str

    model_config = SettingsConfigDict(env_file='.env/db.env')

    def get_db_url(self):
        return f'sqlite+aiosqlite:///{self.DB_PATH}'


settings = Settings()
DB_URL = settings.get_db_url()
engine = create_async_engine(DB_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def create_db_and_tables():
    return Base.metadata.create_all(engine)