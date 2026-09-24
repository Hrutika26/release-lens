from db.repositories import Repositories
from models.release import Release
from models.release_environment import ReleaseEnvironment
from schemas.release import ReleaseDetailResponse, ReleaseSummaryResponse
from schemas.release_environment import ReleaseEnvironmentResponse
from schemas.endpoint_metric import EndpointMetricResponse


class ReleaseService:
    def __init__(self, repositories: Repositories):
        self.release_repository = repositories.release
        self.release_environment_repository = repositories.release_environment
        self.endpoint_metric_repository = repositories.endpoint_metric

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

    async def get_environment_metrics(self, project_id: int, release_id: int, environment_id: int) -> list[EndpointMetricResponse] | None:

        release = await self.get_release(
            project_id=project_id,
            release_id=release_id,
        )

        if release is None:
            return None

        environment = (
            await self.release_environment_repository
            .find_by_id(environment_id)
        )

        if (
            environment is None
            or environment.release_id != release_id
        ):
            return None

        metrics = (
            await self.endpoint_metric_repository
            .find_all_by_release_environment(
                environment_id
            )
        )

        return [
            EndpointMetricResponse(
                endpoint=metric.endpoint,
                method=metric.method,
                request_count=metric.request_count,
                average_latency=metric.average_latency,
                p50_latency=metric.p50_latency,
                p95_latency=metric.p95_latency,
                p99_latency=metric.p99_latency,
                error_rate=metric.error_rate,
                client_error_rate=metric.client_error_rate,
                server_error_rate=metric.server_error_rate,
                additional_metrics=metric.additional_metrics,
                metrics_version=metric.metrics_version,
            )
            for metric in metrics
        ]

    async def get_release_detail(self, project_id: int, release_id: int) -> ReleaseDetailResponse | None:

        release = await self.release_repository.find_by_id(
            release_id
        )

        if (
            release is None
            or release.project_id != project_id
        ):
            return None

        environments = (
            await self.release_environment_repository
            .find_all_by_release(release_id)
        )

        return ReleaseDetailResponse(
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
            