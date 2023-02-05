from aiogram import Dispatcher
from aiogram.types import Message

from keyboards.keyboards import *

from products.products import get_products


# Начальное меню
async def process_start_command(message: Message):
    await message.answer(text='Выбери интересующую категорию', reply_markup=start_keyboard)


# Б/У устройства
async def show_used(message: Message):
    response = await get_products(None, "Used")
    await message.answer(text=f'Вот что у нас есть из Б/У устройств\n{response}',
                         reply_markup=main_or_contact_keyboard)


# Новые в наличии или под заказ
async def stock_order(message: Message):
    await message.answer(text='Посмотри что есть в наличии. Если не найдешь то, что тебе нужно, под заказ срок доставки'
                              ' 4 дня', reply_markup=choose_keyboard)


# Новые в наличии
async def new_stock(message: Message):
    response = await get_products(None, "New_stock")
    await message.answer(text=f'Вот что есть в наличии из новых.\n'
                              f'{response}',
                         reply_markup=back_contact_keyboard)


# Категории новых устройств под заказ
async def new_order(message: Message):
    await message.answer(text='Что именно интересует?', reply_markup=new_categories_keyboard)


# Выбор модели iPhone
async def choose_iphone_category(message: Message):
    await message.answer(text='Выбирай', reply_markup=iphone_keyboard)


# Цена на выбранные модели iPhone под заказ
async def iphone_price(message: Message):
    response = await get_products(message.text, "New_order")
    await message.answer(text=f'Вот цены под заказ на выбранные модели\n{response}',
                         reply_markup=iphone_contact_keyboard)


# Цена на выбранную категорию под заказ
async def other_new_price(message: Message):
    response = await get_products(message.text.strip('📱📲💻⌚️🎧 '), "New_order")
    await message.answer(text=f'Цены на товары из категории {message.text}'
                              f'{response}',
                         reply_markup=category_contact_keyboard)


# Связь с менеджером
async def contact(message: Message):
    await message.answer(text='А тут ничего нет')


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands='start', text='⬅️ Главное меню')
    dp.register_message_handler(show_used, text='Б/У Устройства')
    dp.register_message_handler(stock_order, text=['Новые устройства', '⬅️ Назад'])
    dp.register_message_handler(new_stock, text='В наличии')
    dp.register_message_handler(new_order, text=['Под заказ', '⬅️ Назад к выбору категории'])
    dp.register_message_handler(choose_iphone_category, text=['📱 iPhone', '⬅️ Назад к выбору модели'])
    dp.register_message_handler(iphone_price, text=['iPhone 11/Pro/Max', 'iPhone 12/Pro/Max',
                                                    'iPhone 13/Pro/Max', 'iPhone 14/Pro/Max'])
    dp.register_message_handler(other_new_price, text=['📲 iPad', '💻 MacBook', '⌚️ Watch',
                                                       '🎧 AirPods', 'Прочие устройства'])
    dp.register_message_handler(contact, text='Написать менеджеру')
