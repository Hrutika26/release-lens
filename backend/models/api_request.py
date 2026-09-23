from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApiRequest:
    id: int
    release_environment_id: int
    request_id: str
    timestamp: datetime
    endpoint: str
    method: str
    status_code: int
    response_time_ms: int
    created_at: datetime