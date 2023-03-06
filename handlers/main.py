import requests
from aiogram import Router, F, types
from aiogram.filters import CommandStart, Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from api.query import get_groups_list, get_price, get_products_to_order, get_user_orders
from api.titles_lists import product_groups, products_list
from db.users import create_user, get_user, User
from helper import parse_name_to_kwargs
from keyboards.main import category_kb, main_kb, order_kb, custom_kb
from config import PAYMENTS_TOKEN
from order.create_order import create_order

router: Router = Router()


class OrderStates(StatesGroup):
    waiting_for_group = State()
    view_price = State()
    waiting_order = State()
    payment = State()
    registration = State()


@router.message(CommandStart())
async def start_menu(message: Message, session_maker: sessionmaker, state: FSMContext):
    if not await get_user(user_id=message.from_user.id, session_maker=session_maker):
        await create_user(user_id=message.from_user.id,
                          username=message.from_user.username,
                          session_maker=session_maker)
    await state.set_state(OrderStates.waiting_for_group)
    await message.answer(text='гыгык', reply_markup=main_kb())


@router.message(Text(text='Главное меню'))
async def main_menu(message: Message, state: FSMContext):
    await state.set_state(OrderStates.waiting_for_group)
    await message.answer(text='гыгык', reply_markup=main_kb())


@router.message(Text(text='Профиль'))
async def user_profile(message: Message, session_maker: sessionmaker):
    user_orders = await get_user_orders(user_id=message.from_user.id, session_maker=session_maker)
    if not user_orders:
        await message.answer(text="У тебя еще нет активных заказов", reply_markup=custom_kb("Главное меню"))
    else:
        text = '\n'.join(user_orders)
        await message.answer(text=text, reply_markup=custom_kb("Главное меню"))


# Меню групп техники
@router.message(OrderStates.waiting_for_group, Text(text=product_groups))
async def groups_menu(message: Message, state: FSMContext):
    groups = get_groups_list()
    if not any(map(lambda x: x['pathName'].endswith(message.text), groups)):
        await message.answer(text=f"Вот что у нас есть:\n\n"
                                  f"{get_price(message.text)}\n\n"
                                  f"Если хочешь заказать позицию, которой нет в наличии нажми на кнопку 'Оформить заказ'",
                             reply_markup=custom_kb("Оформить заказ"))
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
                await message.answer(text="Выбери товар, который хочешь заказать",
                                     reply_markup=order_kb(data.get('products')))
                await state.set_state(OrderStates.waiting_order)
            else:
                await message.answer(text='Для оформления заказа необходимо зарегистрироваться.',
                                     reply_markup=custom_kb("Регистрация")
                                     )
                await state.set_state(OrderStates.registration)


@router.message(OrderStates.waiting_order, Text(text=products_list))
async def new_order(message: Message, state: FSMContext):
    product = parse_name_to_kwargs(message.text)
    price = LabeledPrice(label=product.get('name'), amount=product.get('price')/100) # Деление на 100 для тестового платежа
    await message.answer_invoice(
        title=product.get('name'),
        description='Описание',
        provider_token=PAYMENTS_TOKEN,
        currency='rub',
        is_flexible=False,
        prices=[price],
        payload='шляпа',
    )
    await state.set_state(OrderStates.payment)
    await state.update_data(selected_product=message.text)


@router.pre_checkout_query(OrderStates.payment)
async def pre_checkout(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True, error_message='Что-то пошло не так, попробуй позже.')


@router.message(F.successful_payment, OrderStates.payment)
async def successful_payment(message: Message, session_maker:sessionmaker, state: FSMContext):
    data = await state.get_data()
    await create_order(product=data.get('selected_product'), user_id=message.from_user.id, session_maker=session_maker)
    await message.answer(text=f"Платеж на сумму {message.successful_payment.total_amount // 100} "
                              f"{message.successful_payment.currency} прошел успешно. Статус заказа можешь посмотреть"
                              f"в профиле.", reply_markup=custom_kb("Главное меню", "Профиль"))
    await state.clear()
