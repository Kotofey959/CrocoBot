import requests
from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from api.query import get_groups_list, get_price, get_products_to_order
from db.users import create_user, is_user_reg, User
from keyboards.main import category_kb, main_kb, products_kb, pre_order_kb, order_kb, reg_kb

router: Router = Router()


class OrderStates(StatesGroup):
    waiting_for_group = State()
    view_price = State()
    waiting_order = State()
    payment = State()


@router.message(CommandStart())
async def start_menu(message: Message, session_maker: sessionmaker, state: FSMContext):
    if not await is_user_reg(user_id=message.from_user.id, session_maker=session_maker):
        await create_user(user_id=message.from_user.id,
                          username=message.from_user.username,
                          session_maker=session_maker)
    await state.set_state(OrderStates.waiting_for_group)
    await message.answer(text='гыгык', reply_markup=main_kb())


# Меню групп техники
@router.message(OrderStates.waiting_for_group)
async def groups_menu(message: Message, state: FSMContext):
    groups = get_groups_list()
    if not any(map(lambda x: x['pathName'].endswith(message.text), groups)):
        await message.answer(text=f"Вот что у нас есть:\n\n"
                                  f"{get_price(message.text)}\n\n"
                                  f"Если хочешь заказать позицию, которой нет в наличии нажми на кнопку 'Оформить заказ'",
                             reply_markup=pre_order_kb())
        await state.set_state(OrderStates.view_price)
        await state.update_data(products=get_products_to_order(message.text))
    else:
        await message.answer(text='Выбери интересующую категорию', reply_markup=category_kb(message.text))


@router.message(OrderStates.view_price, Text(text='Оформить заказ'))
async def order_menu(message: Message, state: FSMContext, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).filter_by(user_id=message.from_user.id))
            user: User = sql_res.scalar()
            db_user = user
            if user.crm_link is not None:
                data = await state.get_data()
                await message.answer(text="Выбери товар, который хочешь заказать", reply_markup=order_kb(data['products']))
                await state.set_state(OrderStates.waiting_order)
            else:
                await message.answer(text='Для оформления заказа необходимо зарегистрироваться.', reply_markup=reg_kb())


@router.message(OrderStates.waiting_order)
async def new_order(message: Message, state: FSMContext, session_maker: sessionmaker):
    pass