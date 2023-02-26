import requests
from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from api.link import CRMLink
from config import CRM_API_KEY
from db.users import create_user, is_user_reg
from keyboards.main import categories_list, category_kb, main_kb, products_kb

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
        'Authorization': CRM_API_KEY,
    }
    response = requests.get(CRMLink().productfolder_link, headers=headers).json()
    groups = [group for group in response['rows']]
    if not any(map(lambda x: x['pathName'].endswith(message.text), groups)):
        await message.answer(text='Вот что у нас есть', reply_markup=products_kb(message.text))
    else:
        await message.answer(text='Выбери интересующую категорию', reply_markup=category_kb(message.text))


