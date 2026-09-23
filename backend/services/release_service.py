from db.repositories import Repositories
from models.release import Release
from models.release_environment import ReleaseEnvironment
from schemas.release import ReleaseSummaryResponse
from schemas.release_environment import ReleaseEnvironmentResponse


class ReleaseService:
    def __init__(self, repositories: Repositories):
        self.release_repository = repositories.release
        self.release_environment_repository = repositories.release_environment

    async def get_releases_by_project(self, project_id: int) -> list[Release]:
        return await self.release_repository.find_all_by_project(project_id)

    async def get_release(self, project_id: int, release_id: int) -> Release | None:
        release = await self.release_repository.find_by_id(release_id)

        if release is None:
            return None

        if release.project_id != project_id:
            return None

        return release

    async def get_release_environments(self, project_id: int, release_id: int) -> list[ReleaseEnvironment] | None:
        release = await self.get_release(project_id, release_id)

        if release is None:
            return None

        return await self.release_environment_repository.find_all_by_release(release_id)

    async def get_releases_by_project(self, project_id: int) -> list[ReleaseSummaryResponse]:
        releases = await self.release_repository.find_all_by_project(project_id)

        result: list[ReleaseSummaryResponse] = []

        for release in releases:
            environments = (
                await self.release_environment_repository
                .find_all_by_release(release.id)
            )

            result.append(
                ReleaseSummaryResponse(
                    id=release.id,
                    project_id=release.project_id,
                    version=release.version,
                    commit_sha=release.commit_sha,
                    created_at=release.created_at,
                    updated_at=release.updated_at,

                    environments=[
                        ReleaseEnvironmentResponse(
                            id=environment.id,
                            release_id=environment.release_id,
                            environment=environment.environment,
                            deployed_at=environment.deployed_at,
                            created_at=environment.created_at,
                            updated_at=environment.updated_at,
                        )
                        for environment in environments
                    ],
                )
            )

        return result
        