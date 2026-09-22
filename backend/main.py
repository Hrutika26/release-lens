from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from db.connection import create_db_pool
from db.migrations import run_migrations
from api.projects import router as project_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await create_db_pool()

    await run_migrations(app.state.db_pool)

    yield

    await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello" : "ME!"}

@app.get("/health/db")
async def database_health(request: Request):
    try:
        pool = request.app.state.db_pool

        async with pool.acquire() as connection:
            result = await connection.fetchval("SELECT 1")

        if result == 1:
            return {
                "status": "success",
                "message": "Database connection successful",
            }

        return {
            "status": "error",
            "message": "Database connection failed",
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Database connection failed",
            "error": str(e),
        }

app.include_router(project_router)

