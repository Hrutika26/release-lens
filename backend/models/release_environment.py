from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReleaseEnvironment:
    id: int
    release_id: int
    environment: str
    deployed_at: datetime | None
    created_at: datetime
    updated_at: datetime