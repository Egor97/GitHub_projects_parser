from logging import getLogger
from typing import Annotated

import asyncpg
from asyncpg import Pool, Connection
from fastapi import Depends

from app.config import settings

logger = getLogger(__name__)

connection_pool: Pool | None = None


async def create_connection_pool():
    global connection_pool
    logger.debug('Create connection pool')
    try:
        connection_pool = await asyncpg.create_pool(dsn=str(settings.SQLALCHEMY_DATABASE_URI), max_size=20)
    except Exception as ex:
        logger.exception(ex)

    return connection_pool


async def get_session() -> Connection:
    async with connection_pool.acquire() as session:
        yield session


async def close_connection_pool():
    logger.debug('Close connection pool')
    if connection_pool:
        await connection_pool.close()


DatabaseDep = Annotated[Pool, Depends(get_session)]
