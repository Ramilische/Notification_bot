import asyncio
import sys
from os import getenv
import dotenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from db_scripts.db import do, get_one, get_many
from db_scripts import (
    user as crud_user,
    profile as crud_profile,
    website as crud_website,
    form as crud_form
)

dotenv.load_dotenv(dotenv.find_dotenv('.env/creds.env'))
TOKEN = getenv('TELEGRAM_BOT_TOKEN')
HELP_TEXT = open('data/help.txt', 'r', encoding='utf-8').read()

dp = Dispatcher()


async def add_user(message: Message):
    user_info = message.from_user
    if await get_one(crud_user.get_user_by_id, user_info.id) is None:
        await do(
            crud_user.add_user,
            chat_id=user_info.id,
            username=user_info.username,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            is_admin=False,
        )


@dp.message(Command('start'))
async def command_start_handler(message: Message):
    await add_user(message)
    await message.answer('Я асинхронный бот на aiogram')


@dp.message(Command('help'))
async def command_help_handler(message: Message):
    await message.answer(HELP_TEXT)


@dp.message(Command('shutdown'))
async def command_shutdown_handler(message: Message):
    await message.answer('Завершаю работу')
    print('Администратор завершил работу бота')
    sys.exit(0)


#   Запуск бота
async def main():
    try:
        bot = Bot(token=TOKEN)
        print('Бот начал работать. Нажми Ctrl + C чтобы остановить работу')
    except Exception as e:
        print(e)
        print('Бот не запустился')
        sys.exit(1)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Работа бота завершена принудительно')