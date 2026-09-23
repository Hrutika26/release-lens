from dataclasses import dataclass
from datetime import datetime


@dataclass
class Release:
    id: int
    project_id: int
    version: str
    commit_sha: str | None
    created_at: datetime
    updated_at: datetime