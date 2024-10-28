from logging import getLogger
from typing import Annotated

import asyncpg
from asyncpg import Pool
from fastapi import Depends

from app.config import settings

logger = getLogger(__name__)


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Database:
    connection_pool: Pool | None = None

    @classmethod
    async def get_connection_pool(cls):
        if not cls.connection_pool:
            logger.debug('Trying to connect to database')
            try:
                cls.connection_pool: Pool = await asyncpg.create_pool(dsn=str(settings.SQLALCHEMY_DATABASE_URI),
                                                                      max_size=20)
            except Exception as ex:
                logger.exception(ex)
                raise ex
            logger.debug('Success')

        return cls.connection_pool

    @classmethod
    async def close_connection(cls):
        logger.debug('Close connection')
        if cls.connection_pool:
            await cls.connection_pool.close()


async def get_pool() -> Pool:
    database = Database()
    pool = await database.get_connection_pool()
    return pool


DatabaseDep = Annotated[Pool, Depends(get_pool)]
