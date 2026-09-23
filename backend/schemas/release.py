from datetime import datetime

from pydantic import BaseModel


class ReleaseResponse(BaseModel):
    id: int
    project_id: int
    version: str
    commit_sha: str | None
    created_at: datetime
    updated_at: datetime