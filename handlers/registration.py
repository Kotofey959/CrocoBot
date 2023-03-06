import re

from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from config import PHONE_REG, USER_NAME_REG
from db import User
from order.user_registration import register_user

from keyboards.main import share_phone, order_kb

from .main import OrderStates

router = Router()


class RegStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()


@router.message(OrderStates.registration, Text(text='Регистрация'))
async def start_reg(message: Message, state: FSMContext):
    await message.answer(text='Давай пройдем быструю регистрацию. Введи свою фамилию и имя')
    await state.set_state(RegStates.waiting_for_name)


@router.message(RegStates.waiting_for_name)
async def name_reg(message: Message, state: FSMContext, session_maker: sessionmaker):
    if not re.match(USER_NAME_REG, message.text):
        await message.answer(text='Введи фамилию и имя в формате Иванов Иван')
        return

    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).filter_by(user_id=message.from_user.id))
            user: User = sql_res.scalar()
            user.name = message.text
            await state.set_state(RegStates.waiting_for_phone)
            await message.answer(text='Теперь введи свой номер телефона', reply_markup=share_phone())


@router.message(RegStates.waiting_for_phone)
async def phone_reg(message: Message, state: FSMContext, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).filter_by(user_id=message.from_user.id))
            user: User = sql_res.scalar()
            if message.contact:
                user.phone_number = int(message.contact.phone_number)
            else:
                if not re.match(PHONE_REG, message.text):
                    await message.answer(text='Введи номер телефона в формате 89991234567')
                    return
                user.phone_number = int(message.text)
            user.crm_link = await register_user(user.name, user.phone_number)
            await state.set_state(OrderStates.waiting_order)
            data = await state.get_data()
            await message.answer(text='Регистрация прошла успешно. Теперь выбери товар который хочешь заказать.',
                                 reply_markup=order_kb(data['products']))