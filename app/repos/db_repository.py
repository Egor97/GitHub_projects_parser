from datetime import date
from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlalchemy.exc import DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import DatabaseDep
from app.repos.models import Repository
from app.utils import SortDep, OrderDep


class DbRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_repositories(self, filters: SortDep, order: OrderDep) -> list[Repository]:
        # await self.session.
        # fields = ', '.join([field.name for field in sorted_fields])
        #
        # query = f"SELECT repo, owner, position_cur, position_prev, stars,watchers, " \
        #         f"forks, open_issues, language FROM repo ORDER BY {fields} {order.value};"
        #
        # return await self.session.fetch(query)
        print([x_filter.name for x_filter in filters])
        stmt = select(Repository).order_by()
        return list((await self.session.execute(stmt)).scalars())

    async def check_repo_name(self, repo_name) -> bool:
        res = await self.session.fetchrow('SELECT EXISTS (SELECT repo FROM activity WHERE repo = $1)', repo_name)
        return res['exists']

    async def get_repository_activity(self, name: str, since: date, until: date) -> list[str]:
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

    async def check(self):
        query = (await self.session.execute(text("select 1;"))).scalar_one_or_none()
        return query

    async def create_repository(self, repository: Repository):
        self.session.add(repository)
        try:
            await self.session.commit()
        except Exception as ex:
            await self.session.rollback()
            raise ex


async def get_repository(pool: DatabaseDep) -> DbRepository:
    return DbRepository(pool)


RepositoryDep = Annotated[DbRepository, Depends(get_repository)]
