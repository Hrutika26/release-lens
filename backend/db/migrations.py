import re
from pathlib import Path

import asyncpg


MIGRATIONS_DIR = Path(__file__).parent / "migrations"

MIGRATION_FILE_PATTERN = re.compile(
    r"^V_(\d+)__(.+)\.sql$"
)


def extract_migration_version(file_path: Path) -> int:
    match = MIGRATION_FILE_PATTERN.match(file_path.name)

    if not match:
        raise ValueError(
            f"Invalid migration filename: {file_path.name}. "
            "Expected format: V_<version>__<description>.sql"
        )

    return int(match.group(1))


def get_migration_files() -> list[Path]:
    migration_files = list(MIGRATIONS_DIR.glob("V_*.sql"))

    return sorted(
        migration_files,
        key=extract_migration_version,
    )


async def create_migration_table(connection: asyncpg.Connection) -> None:
    await connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version BIGINT PRIMARY KEY,
            filename TEXT NOT NULL,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """
    )


async def get_applied_versions(connection: asyncpg.Connection) -> set[int]:
    
    rows = await connection.fetch(
        """
        SELECT version
        FROM schema_migrations;
        """
    )

    return {
        row["version"]
        for row in rows
    }


async def run_migrations(pool: asyncpg.Pool) -> None:
   
    async with pool.acquire() as connection:
        await create_migration_table(connection)

        applied_versions = await get_applied_versions(
            connection
        )

        migration_files = get_migration_files()

        for migration_file in migration_files:
            version = extract_migration_version(
                migration_file
            )

            if version in applied_versions:
                continue

            sql = migration_file.read_text(
                encoding="utf-8"
            )

            print(
                f"Applying migration "
                f"V_{version}: {migration_file.name}"
            )

            async with connection.transaction():
                await connection.execute(sql)

                await connection.execute(
                    """
                    INSERT INTO schema_migrations (
                        version,
                        filename
                    )
                    VALUES ($1, $2);
                    """,
                    version,
                    migration_file.name,
                )

            print(
                f"Applied migration "
                f"V_{version}: {migration_file.name}"
            )

        print("Database migrations complete.")