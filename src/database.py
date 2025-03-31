from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL, echo=False)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

#from sqlalchemy import text
#import asyncio
# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text("SELECT version()"))
#         print(res.fetchone())

# asyncio.run(func())

