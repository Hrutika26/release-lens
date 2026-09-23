from datetime import datetime

from pydantic import BaseModel


class ReleaseEnvironmentResponse(BaseModel):
    id: int
    release_id: int
    environment: str
    deployed_at: datetime | None
    created_at: datetime
    updated_at: datetime