from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from order.user_registration import register_user
import re

from db import User

router: Router = Router()

phone_regular = '^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
name_regular = '^[А-ЯЁ][а-яё]* [А-ЯЁ][а-яё]*$'


class RegStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()


@router.message(Text(text='Регистрация'))
async def start_reg(message: Message, state: FSMContext):
    await message.answer(text='Давай пройдем быструю регистрацию. Введи свою фамилию и имя')
    await state.set_state(RegStates.waiting_for_name)


@router.message(RegStates.waiting_for_name)
async def name_reg(message: Message, state: FSMContext, session_maker: sessionmaker):
    if re.match(name_regular, message.text):
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(select(User).filter_by(user_id=message.from_user.id))
                user: User = sql_res.scalar()
                user.name = message.text
                await state.set_state(RegStates.waiting_for_phone)
                await message.answer(text='Теперь введи свой номер телефона')
    else:
        await message.answer(text='Введи фамилию и имя в формате Иванов Иван')


@router.message(RegStates.waiting_for_phone)
async def phone_reg(message: Message, state: FSMContext, session_maker: sessionmaker):
    if re.match(phone_regular, message.text):
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(select(User).filter_by(user_id=message.from_user.id))
                user: User = sql_res.scalar()
                user.phone_number = int(message.text)
                user.crm_link = await register_user(user.name, user.phone_number)
                await state.clear()
                await message.answer(text='Регистрация прошла успешно')
    else:
        await message.answer(text='Введи номер телефона в формате 89991234567')