from db.repositories import Repositories
from schemas.release_comparison import EndpointComparisonResponse,MetricValueResponse,ReleaseComparisonSummaryResponse,ReleaseEnvironmentComparisonResponse


class ReleaseComparisonService:
    def __init__(
        self,
        repositories: Repositories,
    ):
        self.release_repository = repositories.release
        self.release_environment_repository = (
            repositories.release_environment
        )
        self.endpoint_metric_repository = (
            repositories.endpoint_metric
        )


    async def compare(
        self,
        project_id: int,
        base_environment_id: int,
        target_environment_id: int,
    ) -> ReleaseEnvironmentComparisonResponse:

        base_environment = (
            await self.release_environment_repository
            .find_by_id(base_environment_id)
        )

        target_environment = (
            await self.release_environment_repository
            .find_by_id(target_environment_id)
        )

        if (
            base_environment is None
            or target_environment is None
        ):
            raise ValueError(
                "Release environment not found."
            )


        base_release = (
            await self.release_repository.find_by_id(
                base_environment.release_id
            )
        )

        target_release = (
            await self.release_repository.find_by_id(
                target_environment.release_id
            )
        )

        if (
            base_release is None
            or target_release is None
        ):
            raise ValueError(
                "Release not found."
            )


        # Both releases must belong to the same project.
        if (
            base_release.project_id != project_id
            or target_release.project_id != project_id
        ):
            raise ValueError(
                "Releases do not belong to this project."
            )


        # Do not compare the exact same release.
        if base_release.id == target_release.id:
            raise ValueError(
                "Base and target releases must be different."
            )


        # v1.4 production vs v1.5 production ✅
        # v1.4 staging vs v1.5 production ❌
        if (
            base_environment.environment
            != target_environment.environment
        ):
            raise ValueError(
                "Release environments must match."
            )


        base_summary = (
            await self.endpoint_metric_repository
            .get_environment_summary(
                base_environment.id
            )
        )

        target_summary = (
            await self.endpoint_metric_repository
            .get_environment_summary(
                target_environment.id
            )
        )


        base_metrics = (
            await self.endpoint_metric_repository
            .find_all_by_release_environment(
                base_environment.id
            )
        )

        target_metrics = (
            await self.endpoint_metric_repository
            .find_all_by_release_environment(
                target_environment.id
            )
        )


        summary = ReleaseComparisonSummaryResponse(
            total_requests=self._compare_metric(
                self._get_value(
                    base_summary,
                    "total_requests",
                ),
                self._get_value(
                    target_summary,
                    "total_requests",
                ),
            ),

            average_latency=self._compare_metric(
                self._get_value(
                    base_summary,
                    "average_latency",
                ),
                self._get_value(
                    target_summary,
                    "average_latency",
                ),
            ),

            p95_latency=self._compare_metric(
                self._get_value(
                    base_summary,
                    "p95_latency",
                ),
                self._get_value(
                    target_summary,
                    "p95_latency",
                ),
            ),

            p99_latency=self._compare_metric(
                self._get_value(
                    base_summary,
                    "p99_latency",
                ),
                self._get_value(
                    target_summary,
                    "p99_latency",
                ),
            ),

            error_rate=self._compare_metric(
                self._get_value(
                    base_summary,
                    "error_rate",
                ),
                self._get_value(
                    target_summary,
                    "error_rate",
                ),
            ),
        )


        endpoint_comparisons = (
            self._compare_endpoints(
                base_metrics,
                target_metrics,
            )
        )


        return ReleaseEnvironmentComparisonResponse(
            base_release_id=base_release.id,
            base_release_environment_id=(
                base_environment.id
            ),
            base_version=base_release.version,

            target_release_id=target_release.id,
            target_release_environment_id=(
                target_environment.id
            ),
            target_version=target_release.version,

            environment=target_environment.environment,

            summary=summary,

            endpoints=endpoint_comparisons,
        )


    def _compare_endpoints(
        self,
        base_metrics,
        target_metrics,
    ) -> list[EndpointComparisonResponse]:

        base_map = {
            (
                metric.method,
                metric.endpoint,
            ): metric
            for metric in base_metrics
        }

        target_map = {
            (
                metric.method,
                metric.endpoint,
            ): metric
            for metric in target_metrics
        }


        endpoint_keys = (
            set(base_map.keys())
            | set(target_map.keys())
        )


        comparisons: list[
            EndpointComparisonResponse
        ] = []


        for method, endpoint in sorted(
            endpoint_keys
        ):
            base = base_map.get(
                (method, endpoint)
            )

            target = target_map.get(
                (method, endpoint)
            )


            comparisons.append(
                EndpointComparisonResponse(
                    endpoint=endpoint,
                    method=method,

                    request_count=(
                        self._compare_metric(
                            (
                                base.request_count
                                if base
                                else None
                            ),
                            (
                                target.request_count
                                if target
                                else None
                            ),
                        )
                    ),

                    average_latency=(
                        self._compare_metric(
                            (
                                base.average_latency
                                if base
                                else None
                            ),
                            (
                                target.average_latency
                                if target
                                else None
                            ),
                        )
                    ),

                    p50_latency=(
                        self._compare_metric(
                            (
                                base.p50_latency
                                if base
                                else None
                            ),
                            (
                                target.p50_latency
                                if target
                                else None
                            ),
                        )
                    ),

                    p95_latency=(
                        self._compare_metric(
                            (
                                base.p95_latency
                                if base
                                else None
                            ),
                            (
                                target.p95_latency
                                if target
                                else None
                            ),
                        )
                    ),

                    p99_latency=(
                        self._compare_metric(
                            (
                                base.p99_latency
                                if base
                                else None
                            ),
                            (
                                target.p99_latency
                                if target
                                else None
                            ),
                        )
                    ),

                    error_rate=(
                        self._compare_metric(
                            (
                                base.error_rate
                                if base
                                else None
                            ),
                            (
                                target.error_rate
                                if target
                                else None
                            ),
                        )
                    ),

                    client_error_rate=(
                        self._compare_metric(
                            (
                                base.client_error_rate
                                if base
                                else None
                            ),
                            (
                                target.client_error_rate
                                if target
                                else None
                            ),
                        )
                    ),

                    server_error_rate=(
                        self._compare_metric(
                            (
                                base.server_error_rate
                                if base
                                else None
                            ),
                            (
                                target.server_error_rate
                                if target
                                else None
                            ),
                        )
                    ),
                )
            )


        return comparisons


    @staticmethod
    def _compare_metric(
        base_value: float | int | None,
        target_value: float | int | None,
    ) -> MetricValueResponse:

        if (
            base_value is None
            or target_value is None
        ):
            return MetricValueResponse(
                base_value=base_value,
                target_value=target_value,
                absolute_delta=None,
                percentage_delta=None,
            )


        absolute_delta = (
            target_value - base_value
        )


        percentage_delta = None

        if base_value != 0:
            percentage_delta = (
                absolute_delta
                / base_value
            ) * 100


        return MetricValueResponse(
            base_value=float(base_value),
            target_value=float(target_value),
            absolute_delta=float(
                absolute_delta
            ),
            percentage_delta=(
                float(percentage_delta)
                if percentage_delta is not None
                else None
            ),
        )


    @staticmethod
    def _get_value(
        summary: dict | None,
        key: str,
    ):
        if summary is None:
            return None

        return summary.get(key)