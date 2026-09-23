from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ApiRequestImport(BaseModel):
    type: Literal["request"]

    request_id: str = Field(alias="requestId", min_length=1, max_length=255)

    timestamp: datetime

    endpoint: str = Field(min_length=1, max_length=500)

    method: str = Field(min_length=1, max_length=20)

    status_code: int = Field(alias="statusCode", ge=100, le=599)

    response_time_ms: int = Field(alias="responseTimeMs", ge=0)