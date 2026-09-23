import asyncpg

from models.endpoint_metric import EndpointMetric


class EndpointMetricRepository:
    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def find_all_by_release_environment(self, release_environment_id: int) -> list[EndpointMetric]:
        rows = await self.db.fetch(
            """
            SELECT
                id,
                release_environment_id,
                endpoint,
                method,
                request_count,
                average_latency,
                p50_latency,
                p95_latency,
                p99_latency,
                error_rate,
                client_error_rate,
                server_error_rate,
                additional_metrics,
                metrics_version,
                created_at,
                updated_at
            FROM endpoint_metric
            WHERE release_environment_id = $1
            ORDER BY method, endpoint
            """,
            release_environment_id,
        )

        return [
            EndpointMetric(**dict(row))
            for row in rows
        ]

    async def recalculate_for_release_environment(self, release_environment_id: int, metrics_version: int = 1) -> None:
        await self.db.execute(
            """
            INSERT INTO endpoint_metric (
                release_environment_id,
                endpoint,
                method,
                request_count,
                average_latency,
                p50_latency,
                p95_latency,
                p99_latency,
                error_rate,
                client_error_rate,
                server_error_rate,
                additional_metrics,
                metrics_version
            )
            SELECT
                release_environment_id,
                endpoint,
                method,

                COUNT(*) AS request_count,

                AVG(response_time_ms)::DOUBLE PRECISION
                    AS average_latency,

                percentile_cont(0.50)
                    WITHIN GROUP (
                        ORDER BY response_time_ms
                    )::DOUBLE PRECISION
                    AS p50_latency,

                percentile_cont(0.95)
                    WITHIN GROUP (
                        ORDER BY response_time_ms
                    )::DOUBLE PRECISION
                    AS p95_latency,

                percentile_cont(0.99)
                    WITHIN GROUP (
                        ORDER BY response_time_ms
                    )::DOUBLE PRECISION
                    AS p99_latency,

                (
                    COUNT(*) FILTER (
                        WHERE status_code >= 400
                    ) * 100.0
                    / NULLIF(COUNT(*), 0)
                )::DOUBLE PRECISION
                    AS error_rate,

                (
                    COUNT(*) FILTER (
                        WHERE status_code >= 400
                          AND status_code < 500
                    ) * 100.0
                    / NULLIF(COUNT(*), 0)
                )::DOUBLE PRECISION
                    AS client_error_rate,

                (
                    COUNT(*) FILTER (
                        WHERE status_code >= 500
                    ) * 100.0
                    / NULLIF(COUNT(*), 0)
                )::DOUBLE PRECISION
                    AS server_error_rate,

                '{}'::jsonb
                    AS additional_metrics,

                $2
                    AS metrics_version

            FROM api_request

            WHERE release_environment_id = $1

            GROUP BY
                release_environment_id,
                method,
                endpoint

            ON CONFLICT (
                release_environment_id,
                method,
                endpoint
            )
            DO UPDATE SET
                request_count = EXCLUDED.request_count,
                average_latency = EXCLUDED.average_latency,
                p50_latency = EXCLUDED.p50_latency,
                p95_latency = EXCLUDED.p95_latency,
                p99_latency = EXCLUDED.p99_latency,
                error_rate = EXCLUDED.error_rate,
                client_error_rate = EXCLUDED.client_error_rate,
                server_error_rate = EXCLUDED.server_error_rate,
                additional_metrics = EXCLUDED.additional_metrics,
                metrics_version = EXCLUDED.metrics_version,
                updated_at = CURRENT_TIMESTAMP
            """,
            release_environment_id,
            metrics_version,
        )