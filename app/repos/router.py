from datetime import date
from logging import getLogger
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.repos.schemas import Repo, Activity
from app.repos.service import ServiceDep
from app.utils import OrderType, SortFieldType, SortDep, OrderDep

logger = getLogger()

router = APIRouter(prefix='/repos', tags=['Repos'])


@router.get('/top100')
async def get_top_100(service: ServiceDep,
                      sort_fields: Annotated[list[SortDep], Query()] = SortFieldType.stars,
                      order: OrderDep = OrderType.desc) -> list[Repo]:
    """
    Получить 100 самых популярных репозиториев на GitHub.
    Пример запроса к endpoint'у http://127.0.0.1:8000/api/repos/top100?order=DESC\n
    :param service: Depends\n
    :param sort_fields: list[SortFieldType] - поля сортировки, передаются в виде параметров запроса.
                                    Пример sort_fields=repo. Ограничен перечислением SortFieldType.\n
    :param order: OrderType - порядок сортировки. Пример = order=ASC.\n
    :return: list[Repo] - список сущностей репозитория.\n
    """
    try:
        repositories = await service.get_top(sort_fields, order)
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail='Что-то пошло не так.')

    return repositories


@router.get('/{owner}/{repo}/activity')
async def get_repo_activity(service: ServiceDep, owner: str, repo: str, since: date | None = None,
                            until: date | None = None) -> list[Activity] | None:
    """
    Получить активность репозитория по датам.\n
    :param service: Depends\n
    :param owner: str - Владелец репозитория.\n
    :param repo: str - Имя репозитория\n
    :param since: date - Дата начала поиска активности\n
    :param until: date - Дата конца поиска активности\n
    :return: list[Activity] - список активности репозитория по дням.
    """
    if owner and repo:
        repo_name = f'{owner}/{repo}'
    else:
        raise HTTPException(status_code=400, detail='Не задано имя репозитория или его владелец')

    if since and until:
        if since > until:
            raise HTTPException(status_code=400, detail="Некорректно заданы даты поиска")

    return await service.get_repo_activity(repo_name, since, until)
