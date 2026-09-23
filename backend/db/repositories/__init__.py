import asyncpg

from db.repositories.endpoint_metric_repository import EndpointMetricRepository
from db.repositories.api_request_repository import ApiRequestRepository
from db.repositories.import_job_repository import ImportJobRepository
from db.repositories.release_environment_repository import ReleaseEnvironmentRepository
from db.repositories.release_repository import ReleaseRepository
from db.repositories.project_repository import ProjectRepository


class Repositories:
    def __init__(self, db: asyncpg.Connection):

        self.db = db
        self.project = ProjectRepository(db)
        self.release = ReleaseRepository(db)
        self.release_environment = ReleaseEnvironmentRepository(db)
        self.import_job = ImportJobRepository(db)
        self.api_request = ApiRequestRepository(db)
        self.endpoint_metric = EndpointMetricRepository(db)
        