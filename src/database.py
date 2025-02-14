"""
Modile for database connection
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_session
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator, Any

from .environs import *

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(url=DATABASE_URL)
session = async_sessionmaker(bind=engine, expire_on_commit=True)

class Base(DeclarativeBase):
    """
    Meta class for sqlalchemy ORM models
    """


async def get_db() -> AsyncGenerator[Any, AsyncSession]:
    """
    Courutine for generating db session
    """
    async with async_session() as session:
        yield session