from typing import AsyncGenerator

import asyncpg
from fastapi import Depends, Request

from db.repositories import Repositories
from services.services import Services

async def get_db(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    pool: asyncpg.Pool = request.app.state.db_pool

    async with pool.acquire() as connection:
        yield connection

def get_repositories(db: asyncpg.Connection = Depends(get_db)) -> Repositories:
    return Repositories(db)


def get_services(repositories: Repositories = Depends(get_repositories)) -> Services:
    return Services(repositories)
