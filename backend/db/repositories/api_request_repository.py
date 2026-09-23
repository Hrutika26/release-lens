from collections.abc import Sequence

import asyncpg

from models.api_request import ApiRequest


class ApiRequestRepository:
    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def find_by_id(self, api_request_id: int) -> ApiRequest | None:
        row = await self.db.fetchrow(
            """
            SELECT
                id,
                release_environment_id,
                request_id,
                timestamp,
                endpoint,
                method,
                status_code,
                response_time_ms,
                created_at
            FROM api_request
            WHERE id = $1
            """,
            api_request_id,
        )

        if row is None:
            return None

        return ApiRequest(**dict(row))

    async def find_all_by_release_environment(self, release_environment_id: int) -> list[ApiRequest]:
        rows = await self.db.fetch(
            """
            SELECT
                id,
                release_environment_id,
                request_id,
                timestamp,
                endpoint,
                method,
                status_code,
                response_time_ms,
                created_at
            FROM api_request
            WHERE release_environment_id = $1
            ORDER BY timestamp
            """,
            release_environment_id,
        )

        return [
            ApiRequest(**dict(row))
            for row in rows
        ]

    async def batch_insert(self, release_environment_id: int, requests: Sequence[ApiRequest]) -> None:
        if not requests:
            return

        values = [
            (
                release_environment_id,
                request.request_id,
                request.timestamp,
                request.endpoint,
                request.method,
                request.status_code,
                request.response_time_ms,
            )
            for request in requests
        ]

        await self.db.executemany(
            """
            INSERT INTO api_request (
                release_environment_id,
                request_id,
                timestamp,
                endpoint,
                method,
                status_code,
                response_time_ms
            )
            VALUES (
                $1,
                $2,
                $3,
                $4,
                $5,
                $6,
                $7
            )
            ON CONFLICT (
                release_environment_id,
                request_id
            )
            DO NOTHING
            """,
            values,
        )