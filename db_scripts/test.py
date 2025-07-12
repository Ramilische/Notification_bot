import asyncio
import db
from models import Base, User, Profile, Website, Form
from user import add_user, get_user_by_id, get_user_by_username, update_user, delete_user
import tracemalloc


if __name__ == '__main__':
    # Тест
    # ramilische 98709869
    # result = asyncio.run(db.async_main(get_user_by_username, 'ramilische'))

    #   Добавление юзера если его нет
    # result = asyncio.run(db.async_main(get_user_by_id, 127494))
    # if result is None:
    #     result = asyncio.run(db.async_main(add_user, chat_id=127494, username='ramilka', first_name='ramil', last_name='sharipov'))
    #     print('added user')
    # else:
    #     print('user already exists')
    db.do(delete_user, 127494)
