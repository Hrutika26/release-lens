from datetime import datetime

import asyncpg

from models.release_environment import ReleaseEnvironment


class ReleaseEnvironmentRepository:
    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def find_by_id(self, release_environment_id: int) -> ReleaseEnvironment | None:
        row = await self.db.fetchrow(
            """
            SELECT
                id,
                release_id,
                environment,
                deployed_at,
                created_at,
                updated_at
            FROM release_environment
            WHERE id = $1
            """,
            release_environment_id,
        )

        if row is None:
            return None

        return ReleaseEnvironment(**dict(row))

    async def find_by_release_and_environment(self, release_id: int, environment: str) -> ReleaseEnvironment | None:
        row = await self.db.fetchrow(
            """
            SELECT
                id,
                release_id,
                environment,
                deployed_at,
                created_at,
                updated_at
            FROM release_environment
            WHERE release_id = $1
              AND environment = $2
            """,
            release_id,
            environment,
        )

        if row is None:
            return None

        return ReleaseEnvironment(**dict(row))

    async def find_all_by_release(self, release_id: int) -> list[ReleaseEnvironment]:
        rows = await self.db.fetch(
            """
            SELECT
                id,
                release_id,
                environment,
                deployed_at,
                created_at,
                updated_at
            FROM release_environment
            WHERE release_id = $1
            ORDER BY created_at
            """,
            release_id,
        )

        return [
            ReleaseEnvironment(**dict(row))
            for row in rows
        ]

    async def create(self, release_id: int, environment: str, deployed_at: datetime | None) -> ReleaseEnvironment:
        row = await self.db.fetchrow(
            """
            INSERT INTO release_environment (
                release_id,
                environment,
                deployed_at
            )
            VALUES ($1, $2, $3)
            RETURNING
                id,
                release_id,
                environment,
                deployed_at,
                created_at,
                updated_at
            """,
            release_id,
            environment,
            deployed_at,
        )

        return ReleaseEnvironment(**dict(row))