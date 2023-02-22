from sqlalchemy.ext.asyncio import AsyncSession

from .database import BaseModel
from sqlalchemy import Column, Integer, VARCHAR, Text, select


class User(BaseModel):
    __tablename__ = 'users'
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32),unique=False, nullable=True)
    phone_number = Column(Integer, nullable=True)
    name = Column(Text, nullable=True)
    crm_id = Column(VARCHAR(40), unique=True, nullable=True)

    def __str__(self):
        return f'<User:{self.user_id}>'


async def create_user(user_id, username, session_maker):
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username
            )
            session: AsyncSession
            session.add(user)


async def is_user_reg(user_id, session_maker) -> bool:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.user_id == user_id))
            user: User = sql_res.one_or_none()
            return bool(user)
