from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ReleaseImportMetadata(BaseModel):
    type: Literal["metadata"]

    version: str = Field(min_length=1, max_length=100)

    environment: str = Field(min_length=1, max_length=50)

    deployed_at: datetime | None = Field(default=None, alias="deployedAt")

    commit_sha: str | None = Field(default=None, alias="commitSha", max_length=100)