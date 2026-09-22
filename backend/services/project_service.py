from db.repositories import Repositories
from schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, repositories: Repositories):
        self.repositories = repositories
        self.project_repository = repositories.project

    async def create_project(self, data: ProjectCreate):
        return await self.project_repository.create(
            name=data.name,
            description=data.description,
        )

    async def get_project(self,project_id: int):
        return await self.project_repository.find_by_id(
            project_id
        )

    async def get_projects(self):
        return await self.project_repository.find_all()

    async def update_project(self, project_id: int, data: ProjectUpdate):
        return await self.project_repository.update(
            project_id=project_id,
            name=data.name,
            description=data.description,
        )