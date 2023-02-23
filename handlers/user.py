from aiogram.types import Message
from aiogram import Router
from keyboards.main import categories_list, category_kb, products_kb, main_kb
from aiogram.filters import CommandStart, Text
import requests
from db.users import create_user, is_user_reg
from sqlalchemy.orm import sessionmaker


router: Router = Router()


@router.message(CommandStart())
async def start_menu(message: Message, session_maker: sessionmaker):
    if not await is_user_reg(user_id=message.from_user.id, session_maker=session_maker):
        await create_user(user_id=message.from_user.id,
                          username=message.from_user.username,
                          session_maker=session_maker)
    await message.answer(text='гыгык', reply_markup=main_kb())


# Меню групп техники
@router.message(Text(text=categories_list))
async def groups_menu(message: Message):
    headers = {
        'Authorization': '11b1abf2e30a8a5286cd49a7918aaafccc305096',
    }
    response = requests.get("https://online.moysklad.ru/api/remap/1.2/entity/productfolder",
                            headers=headers).json()
    groups = [group for group in response['rows']]
    if not any(map(lambda x: x['pathName'].endswith(message.text), groups)):
        await message.answer(text='Вот что у нас есть', reply_markup=products_kb(message.text))
    else:
        await message.answer(text='Выбери интересующую категорию', reply_markup=category_kb(message.text))


