from logging import getLogger
from typing import Annotated

import asyncpg
from asyncpg import Pool
from fastapi import Depends

from app.config import settings

logger = getLogger(__name__)


class Database:
    def __init__(self):
        self.connection_pool: Pool | None = None

    async def get_connection_pool(self):
        if not self.connection_pool:
            logger.debug('Trying to connect to database')
            try:
                self.connection_pool: Pool = await asyncpg.create_pool(dsn=str(settings.SQLALCHEMY_DATABASE_URI),
                                                                       max_size=20)
            except Exception as ex:
                logger.exception(ex)
                raise ex
            logger.debug('Success')

        return self.connection_pool

    def close_connection_pool(self):
        if self.connection_pool:
            self.connection_pool.close()


async def get_pool() -> Pool:
    database = Database()
    pool = await database.get_connection_pool()
    return pool

DatabaseDep = Annotated[Pool, Depends(get_pool)]
