import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy import URL

from config import Config, load_config
from handlers import user
from db import create_async_engine, get_session_maker, proceed_schemas, BaseModel


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    postgres_url = URL.create(
        'postgresql+asyncpg',
        username='postgres',
        password='Lol4ik594770146',
        host='localhost',
        port=5432,
        database='Croco_users'

    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    dp.include_router(user.router)

    await dp.start_polling(bot, session_maker=session_maker)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
