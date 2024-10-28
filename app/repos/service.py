from datetime import date
from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException

from app.repos.repository import RepositoryDep, Repository
from app.repos.schemas import Repo, Activity
from app.repos.utils import mapping_repo, mapping_activity
from app.utils import SortDep, OrderDep

logger = getLogger(__name__)


class RepoService:
    def __init__(self, repo):
        self.repo: Repository = repo

    async def get_top(self, sort_fields: SortDep, order: OrderDep) -> list[Repo]:
        logger.debug('Trying to get 100 repositories')
        records = await self.repo.get_repositories(sort_fields, order)

        return [mapping_repo(record) for record in records]

    async def get_repo_activity(self, name: str, since: date, until: date) -> list[Activity] | None:
        logger.debug('Trying to get repository activity')
        logger.debug('Trying to check exists')
        exist = await self.repo.check_repo_name(name)
        if not exist:
            raise HTTPException(status_code=400, detail='Указанного имени репозитория не найдено')

        logger.debug('Trying to get repository activity')
        activities = await self.repo.get_repository_activity(name, since, until)

        return [mapping_activity(activity) for activity in activities]


def get_service(repo: RepositoryDep) -> RepoService:
    return RepoService(repo)


ServiceDep = Annotated[RepoService, Depends(get_service)]
