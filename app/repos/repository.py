from datetime import date
from typing import Annotated

from asyncpg import Record, Connection
from fastapi import Depends

from app.database import DatabaseDep
from app.utils import SortDep, OrderDep


class Repository:
    def __init__(self, session):
        self.session: Connection = session

    async def get_repositories(self, sorted_fields: SortDep, order: OrderDep) -> list[Record]:
        fields = ', '.join([field.name for field in sorted_fields])

        query = f"SELECT repo, owner, position_cur, position_prev, stars,watchers, " \
                f"forks, open_issues, language FROM repo ORDER BY {fields} {order.value};"

        return await self.session.fetch(query)

    async def check_repo_name(self, repo_name) -> bool:
        res = await self.session.fetchrow('SELECT EXISTS (SELECT repo FROM activity WHERE repo = $1)', repo_name)
        return res['exists']

    async def get_repository_activity(self, name: str, since: date, until: date) -> list[Record]:
        query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 ORDER BY date DESC"
        query_params = [name]

        if since and until:
            query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 " \
                    f"AND date BETWEEN $2 AND $3 ORDER BY date DESC"
            query_params += [since, until]
        elif since and not until:
            query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 " \
                    f"AND date >= $2 ORDER BY date DESC"
            query_params.append(since)
        elif not since and until:
            query = f"SELECT date, commits, authors FROM activity WHERE repo = $1 " \
                    f"AND date <= $2 ORDER BY date DESC"
            query_params.append(until)

        return await self.session.fetch(query, *query_params)


async def get_repository(pool: DatabaseDep) -> Repository:
    return Repository(pool)


RepositoryDep = Annotated[Repository, Depends(get_repository)]
