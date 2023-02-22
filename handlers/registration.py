# from aiogram.types import Message
# from aiogram import Router
# from aiogram.filters import Text
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext
# from sqlalchemy.orm import sessionmaker
#
# router: Router = Router()
#
#
# class RegStates(StatesGroup):
#      waiting_for_name = State()
#      waiting_for_phone = State()
#
#
# @router.message(Text(text='Регистрация'))
# async def start_reg(message: Message, state: FSMContext):
#      await message.answer(text='Давай пройдем быструю регистрацию. Введи свою фамилию и имя')
#      await state.set_state(RegStates.waiting_for_name)
#
#
# @router.message(RegStates.waiting_for_name)
# async def name_reg(message: Message, state: FSMContext, session_maker: sessionmaker):
#      async with session_maker() as session:
#          async with session.begin():
#
#
#
#          await state.set_state(RegStates.waiting_for_phone)
#          await message.answer(text='Теперь введи свой номер телефона')
#      else:
#          await message.answer(text='Введи фамилию и имя в формате Иванов Иван')
#
#
# @router.message(RegStates.waiting_for_phone)
# async def phone_reg(message: Message, state: FSMContext):
#      #Если номер валидный, добавляем базу и создаем контрагента в срм
#          await state.clear()
#
#      else:
#          await message.answer(text='Введи номер телефона в формате 89991234567')