from datetime import datetime

from pydantic import BaseModel

from schemas.release_environment import ReleaseEnvironmentResponse


class ReleaseResponse(BaseModel):
    id: int
    project_id: int
    version: str
    commit_sha: str | None
    created_at: datetime
    updated_at: datetime

class ReleaseSummaryResponse(BaseModel):
    id: int
    project_id: int
    version: str
    commit_sha: str | None
    created_at: datetime
    updated_at: datetime

    environments: list[ReleaseEnvironmentResponse]