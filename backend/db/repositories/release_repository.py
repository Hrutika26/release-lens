import asyncpg

from models.release import Release


class ReleaseRepository:
    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def find_by_id(self, release_id: int) -> Release | None:
        row = await self.db.fetchrow(
            """
            SELECT
                id,
                project_id,
                version,
                commit_sha,
                created_at,
                updated_at
            FROM release
            WHERE id = $1
            """,
            release_id,
        )

        if row is None:
            return None

        return Release(**dict(row))

    async def find_by_project_and_version(self, project_id: int, version: str) -> Release | None:
        row = await self.db.fetchrow(
            """
            SELECT
                id,
                project_id,
                version,
                commit_sha,
                created_at,
                updated_at
            FROM release
            WHERE project_id = $1
              AND version = $2
            """,
            project_id,
            version,
        )

        if row is None:
            return None

        return Release(**dict(row))

    async def find_all_by_project(self, project_id: int) -> list[Release]:
        rows = await self.db.fetch(
            """
            SELECT
                id,
                project_id,
                version,
                commit_sha,
                created_at,
                updated_at
            FROM release
            WHERE project_id = $1
            ORDER BY created_at DESC
            """,
            project_id,
        )

        return [
            Release(**dict(row))
            for row in rows
        ]

    async def create(self, project_id: int, version: str, commit_sha: str | None) -> Release:
        row = await self.db.fetchrow(
            """
            INSERT INTO release (
                project_id,
                version,
                commit_sha
            )
            VALUES ($1, $2, $3)
            RETURNING
                id,
                project_id,
                version,
                commit_sha,
                created_at,
                updated_at
            """,
            project_id,
            version,
            commit_sha,
        )

        return Release(**dict(row))