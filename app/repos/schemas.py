from dataclasses import dataclass
from datetime import date


@dataclass
class Repo:
    repo: str
    owner: str
    position_cur: int
    position_prev: int | None
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str | None = None


@dataclass
class Activity:
    date: date
    commits: int
    authors: list[str]
