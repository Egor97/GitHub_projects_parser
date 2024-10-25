from datetime import date
from logging import getLogger
from typing import Annotated

import asyncpg
from asyncpg import Connection, Record
from fastapi import Depends

from app.config import settings
from app.utils import SortDep, OrderDep

logger = getLogger(__name__)


async def init_db_connect():
    logger.debug('Trying to connect to database')
    try:
        conn = await asyncpg.connect(dsn=str(settings.SQLALCHEMY_DATABASE_URI))
    except Exception as ex:
        logger.exception(ex)
        raise ex
    logger.debug('Success')
    return conn


class Repository:
    def __init__(self, session: Connection):
        self.session = session

    async def get_repositories(self, sorted_fields: SortDep, order: OrderDep) -> list[Record]:
        fields = ', '.join([field.name for field in sorted_fields])

        query = f"SELECT repo, owner, position_cur, position_prev, stars,watchers, " \
                f"forks, open_issues, language FROM repo ORDER BY {fields} {order.value};"

        return await self.session.fetch(query)

    async def check_repo_name(self, repo_name) -> bool:
        res = await self.session.fetchrow('SELECT EXISTS (SELECT repo FROM repo WHERE repo = $1)', repo_name)
        return res['exists']

    async def get_repository_activity(self, name: str, since: date, until: date) -> list[Record]:
        query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 ORDER BY date DESC"

        if since and until:
            query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 " \
                    f"AND date BETWEEN $2 AND $3 ORDER BY date DESC"
            return await self.session.fetch(query, name, since, until)
        elif since and not until:
            query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 " \
                    f"AND date >= $2 ORDER BY date DESC"
            return await self.session.fetch(query, name, since)
        elif not since and until:
            query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 " \
                    f"AND date <= $2 ORDER BY date DESC"
            return await self.session.fetch(query, name, until)

        return await self.session.fetch(query, name)


async def get_repository(session=Depends(init_db_connect)) -> Repository:
    return Repository(session)


RepositoryDep = Annotated[Repository, Depends(get_repository)]
