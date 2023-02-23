from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Text
from order.create_order import create_order
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from db import User
router: Router = Router()


@router.message(Text(text='ПОКА ХЗ'))
async def create_new_order(message: Message, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).filter_by(user_id=message.from_user.id))
            user: User = sql_res.scalar()

    await create_order(message.text, user.crm_link)
