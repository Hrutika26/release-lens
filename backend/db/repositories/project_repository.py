import asyncpg

from models.project import Project

class ProjectRepository:
    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def create(self,name: str,description: str | None) -> Project:
        row = await self.db.fetchrow(
            """
            INSERT INTO project (
                name,
                description
            )
            VALUES ($1, $2)
            RETURNING
                id,
                name,
                description,
                created_at,
                updated_at
            """,
            name,
            description,
        )

        return Project(**dict(row))

    async def find_by_id(self, project_id: int) -> Project | None:
        row = await self.db.fetchrow(
            """
            SELECT
                id,
                name,
                description,
                created_at,
                updated_at
            FROM project
            WHERE id = $1
            """,
            project_id,
        )

        if row is None:
            return None

        return Project(**dict(row))

    async def find_all(self) -> list[Project]:
        rows = await self.db.fetch(
            """
            SELECT
                id,
                name,
                description,
                created_at,
                updated_at
            FROM project
            ORDER BY created_at DESC
            """
        )

        return [
            Project(**dict(row))
            for row in rows
        ]

    async def update(self, project_id: int, name: str, description: str | None) -> Project | None:
        row = await self.db.fetchrow(
            """
            UPDATE project
            SET
                name = $2,
                description = $3,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = $1
            RETURNING
                id,
                name,
                description,
                created_at,
                updated_at
            """,
            project_id,
            name,
            description,
        )

        if row is None:
            return None

        return Project(**dict(row))