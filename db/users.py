from sqlalchemy import VARCHAR, Column, Integer, Text, select, BigInteger

from .database import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32),unique=False, nullable=True)
    phone_number = Column(BigInteger, nullable=True)
    name = Column(Text, nullable=True)
    crm_link = Column(VARCHAR, unique=True, nullable=True)

    def __str__(self):
        return f'<User:{self.user_id}>'


async def create_user(user_id, username, session_maker):
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username
            )

            session.add(user)


async def get_user(user_id, session_maker) -> User:
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.user_id == user_id))
            user: User = sql_res.scalar()
            return user


