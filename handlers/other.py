from aiogram import Dispatcher, Router
from aiogram.types import Message

router = Router()


@router.message()
async def send_answer(message: Message):
    await message.answer(text='Я тебя не понимаю, воспользуйся клавиатурой бота.')
