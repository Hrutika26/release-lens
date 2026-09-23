from dataclasses import dataclass
from datetime import datetime


@dataclass
class ImportJob:
    id: int
    project_id: int

    file_name: str
    file_path: str

    version: str
    environment: str

    commit_sha: str | None
    deployed_at: datetime | None

    status: str

    total_records: int
    processed_records: int
    valid_records: int
    invalid_records: int

    error_message: str | None

    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None