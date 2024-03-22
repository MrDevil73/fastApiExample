from config import settings_database
from sqlalchemy.orm import DeclarativeBase, mapped_column
from typing import Annotated

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

async_engine = create_async_engine(
    url=settings_database.DATABASE_URL_asyncpg,
    echo=False,
)
async_session_factory = async_sessionmaker(async_engine)


class Model(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


async def get_or_create(sess, mdl, data):
    instance = await sess.query(mdl).filter_by(**data).first()
    if instance:
        return instance
    else:
        instance = mdl(**data)
        sess.add(instance)
        await sess.commit()
        return instance


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
