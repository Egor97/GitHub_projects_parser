import uuid

from sqlmodel import SQLModel, Field


class Repository(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, unique=True, index=True)
    repo: str = Field(unique=True)
    owner: str
    position_cur: int
    position_prev: int | None
    stars: int
    watchers: int
    forks: int
    open_issues: int
    language: str | None = None

    class Config:
        from_orm = True
        populate_by_name = True

    # activities: list['Activity'] = Relationship(back_populates='repository')

# class Activity(SQLModel, table=True):
#     id: uuid.UUID = Field(primary_key=True)
#     repo: str = Field(foreign_key='repository.repo')
#     authors: ARRAY[str]
#     commits: int
#     date: datetime.date
#
#     repository: DbRepository = Relationship(back_populates='activities')
