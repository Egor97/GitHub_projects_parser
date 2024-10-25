from enum import Enum


class OrderType(Enum):
    asc = "ASC"
    desc = 'DESC'


class SortFieldType(Enum):
    repo = 'repo'
    owner = 'owner'
    position_cur = 'position_cur'
    position_prev = 'position_prev'
    stars = 'stars'
    watchers = 'watchers'
    forks = 'forks'
    open_issues = 'open_issues'
    language = 'language'


SortDep = SortFieldType | None
OrderDep = OrderType | None
