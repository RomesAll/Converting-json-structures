from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from config import settings

engine = create_engine(
    url=settings.database.DATABASE_URL_sync,
    echo=True
)

async_engine = create_async_engine(
    url=settings.database.DATABASE_URL_async,
    echo=True
)

class Base(DeclarativeBase):
    metadata = MetaData()
