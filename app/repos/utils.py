from app.repos.schemas import Repo, Activity


def mapping_repo(record) -> Repo:
    return Repo(*record)


def mapping_activity(record) -> Activity:
    return Activity(*record)
