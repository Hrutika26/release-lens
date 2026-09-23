from datetime import datetime

import asyncpg

from models.import_job import ImportJob


class ImportJobRepository:
    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def create(self, project_id: int, file_name: str, file_path: str,
                        version: str, environment: str, commit_sha: str | None,
                        deployed_at: datetime | None, status: str, total_records: int,
                        valid_records: int, invalid_records: int) -> ImportJob:
        row = await self.db.fetchrow(
            """
            INSERT INTO import_job (
                project_id,
                file_name,
                file_path,
                version,
                environment,
                commit_sha,
                deployed_at,
                status,
                total_records,
                valid_records,
                invalid_records
            )
            VALUES (
                $1, $2, $3, $4, $5, $6,
                $7, $8, $9, $10, $11
            )
            RETURNING
                id,
                project_id,
                file_name,
                file_path,
                version,
                environment,
                commit_sha,
                deployed_at,
                status,
                total_records,
                processed_records,
                valid_records,
                invalid_records,
                error_message,
                created_at,
                started_at,
                completed_at
            """,
            project_id,
            file_name,
            file_path,
            version,
            environment,
            commit_sha,
            deployed_at,
            status,
            total_records,
            valid_records,
            invalid_records,
        )

        return ImportJob(**dict(row))

    async def find_by_id(self, import_id: int) -> ImportJob | None:
        row = await self.db.fetchrow(
            """
            SELECT
                id,
                project_id,
                file_name,
                file_path,
                version,
                environment,
                commit_sha,
                deployed_at,
                status,
                total_records,
                processed_records,
                valid_records,
                invalid_records,
                error_message,
                created_at,
                started_at,
                completed_at
            FROM import_job
            WHERE id = $1
            """,
            import_id,
        )

        if row is None:
            return None

        return ImportJob(**dict(row))

    async def mark_processing(self, import_id: int) -> ImportJob | None:
        row = await self.db.fetchrow(
            """
            UPDATE import_job
            SET
                status = 'PROCESSING',
                started_at = CURRENT_TIMESTAMP,
                error_message = NULL
            WHERE id = $1
            RETURNING
                id,
                project_id,
                file_name,
                file_path,
                version,
                environment,
                commit_sha,
                deployed_at,
                status,
                total_records,
                processed_records,
                valid_records,
                invalid_records,
                error_message,
                created_at,
                started_at,
                completed_at
            """,
            import_id,
        )

        if row is None:
            return None

        return ImportJob(**dict(row))

    async def update_processed_records(self, import_id: int, processed_records: int) -> None:
        await self.db.execute(
            """
            UPDATE import_job
            SET processed_records = $2
            WHERE id = $1
            """,
            import_id,
            processed_records,
        )

    async def mark_completed(self, import_id: int, processed_records: int) -> ImportJob | None:
        row = await self.db.fetchrow(
            """
            UPDATE import_job
            SET
                status = 'COMPLETED',
                processed_records = $2,
                completed_at = CURRENT_TIMESTAMP,
                error_message = NULL
            WHERE id = $1
            RETURNING
                id,
                project_id,
                file_name,
                file_path,
                version,
                environment,
                commit_sha,
                deployed_at,
                status,
                total_records,
                processed_records,
                valid_records,
                invalid_records,
                error_message,
                created_at,
                started_at,
                completed_at
            """,
            import_id,
            processed_records,
        )

        if row is None:
            return None

        return ImportJob(**dict(row))

    async def mark_failed(self, import_id: int, error_message: str) -> ImportJob | None:
        row = await self.db.fetchrow(
            """
            UPDATE import_job
            SET
                status = 'FAILED',
                error_message = $2,
                completed_at = CURRENT_TIMESTAMP
            WHERE id = $1
            RETURNING
                id,
                project_id,
                file_name,
                file_path,
                version,
                environment,
                commit_sha,
                deployed_at,
                status,
                total_records,
                processed_records,
                valid_records,
                invalid_records,
                error_message,
                created_at,
                started_at,
                completed_at
            """,
            import_id,
            error_message,
        )

        if row is None:
            return None

        return ImportJob(**dict(row))