from db.repositories import Repositories
from services.project_service import ProjectService


class Services:
    def __init__(self, repositories: Repositories):
        self.repositories = repositories

        self.project = ProjectService(repositories)