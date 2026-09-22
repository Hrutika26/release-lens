import asyncpg

from db.repositories.project_repository import ProjectRepository


class Repositories:
    def __init__(self, db: asyncpg.Connection):
        self.db = db

        self.project = ProjectRepository(db)