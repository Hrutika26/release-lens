from services.release_comparison_service import ReleaseComparisonService
from services.release_import_service import ReleaseImportService
from services.release_service import ReleaseService
from db.repositories import Repositories
from services.project_service import ProjectService


class Services:
    def __init__(self, repositories: Repositories):

        self.repositories = repositories
        self.project = ProjectService(repositories)
        self.release = ReleaseService(repositories)
        self.release_import = ReleaseImportService(repositories)
        self.release_comparison = ReleaseComparisonService(repositories)
        