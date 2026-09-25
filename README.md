# Release Lens

Track how each release of a service performs in each environment.

Upload an NDJSON file of API traffic for a given version and environment, and Release Lens
stores the raw requests, computes per-endpoint metrics (latency percentiles, error rates),
and lets you compare two releases side by side.

## Architecture

![Release Lens architecture](images/architecture-diagram.png)

Dependencies point one way only: `api-> services-> repositories-> database`.
Routers never write SQL; repositories never know about HTTP.

## Stack

| Layer | Tech |
|---|---|
| Frontend | Angular 19 (standalone components), ng-bootstrap, d3 |
| Backend | FastAPI, asyncpg (raw SQL, no ORM), Pydantic |
| Database | PostgreSQL 17 (Docker) |
| Tooling | uv (Python), npm (Node) |

## Requirements

- Docker
- Python 3.14 + [uv](https://docs.astral.sh/uv/)
- Node 20+

## Running locally

**1. Start Postgres**

```bash
docker compose up -d
```

**2. Start the backend** — runs migrations automatically on boot

```bash
cd backend && uv sync && uv run fastapi dev main.py
```

API on http://localhost:8000 · docs at http://localhost:8000/docs

**3. Start the frontend**

```bash
cd frontend && npm install && npm start
```

App on http://localhost:4200

## Import file format

NDJSON — one JSON object per line. The first line describes the release,
every line after it is a single API request.

```
{"type":"metadata","version":"v1.5","environment":"production","deployedAt":"2026-09-18T14:00:00Z","commitSha":"a84fd21"}
{"type":"request","requestId":"req_001","timestamp":"2026-09-18T14:01:01.482Z","endpoint":"/checkout","method":"POST","statusCode":200,"responseTimeMs":180}
{"type":"request","requestId":"req_002","timestamp":"2026-09-18T14:01:02.104Z","endpoint":"/orders","method":"GET","statusCode":500,"responseTimeMs":420}
```

Import is a two-step flow: **preview** validates the file and reports valid/invalid
record counts, then **confirm** loads it. Re-importing the same file is safe — duplicate
`requestId` values are ignored.

## API

```
GET    /health/db

POST   /projects
GET    /projects
GET    /projects/{id}
PATCH  /projects/{id}

GET    /projects/{id}/releases
GET    /projects/{id}/releases/compare?base_environment_id=&target_environment_id=
GET    /projects/{id}/releases/{release_id}
GET    /projects/{id}/releases/{release_id}/environments/{environment_id}/metrics

POST   /projects/{id}/release-imports/preview
POST   /projects/{id}/release-imports/{import_id}/confirm
GET    /projects/{id}/release-imports/{import_id}
```

## Structure

```
backend/
  api/            HTTP routes, status codes
  services/       business logic, orchestration
  db/repositories/  SQL, one file per table
  db/migrations/  versioned .sql files, applied once each on startup
  models/         dataclasses mirroring table rows
  schemas/        Pydantic request/response shapes
  core/config.py  settings from .env

frontend/src/app/
  features/projects/  pages, models, and the HTTP service
  layout/             sidebar + shell
  shared/             reusable d3 chart
```

Dependencies point one way only: `api-> services-> repositories-> database`.
Routers never write SQL; repositories never know about HTTP.

## Data model

![Database schema](images/schema-design.jpeg)

```
project ──< release ──< release_environment ──< api_request      (raw requests)
   │                            └──────────────< endpoint_metric  (computed rollups)
   └──< import_job
```

Metrics attach to `release_environment` rather than `release`, because the same version
deployed to staging and to production are different deployments with different traffic.

Key constraints:

| Constraint | Purpose |
|---|---|
| `UNIQUE (project_id, version)` | versions are unique within a project, not globally |
| `UNIQUE (release_id, environment)` | one row per version-per-environment |
| `UNIQUE (release_environment_id, request_id)` | makes re-importing a file idempotent |
| `UNIQUE (release_environment_id, method, endpoint)` | one metric row per endpoint; the upsert target |
| `FOREIGN KEY … ON DELETE CASCADE` | deleting a project removes everything it owns |

`schema_migrations` is created by the migration runner and records which versioned
`.sql` files have been applied.

## Configuration

`backend/.env`:

```
DATABASE_URL=postgresql://root:root@localhost:5435/release_lens_db
DB_POOL_MIN_SIZE=5
DB_POOL_MAX_SIZE=20
```
