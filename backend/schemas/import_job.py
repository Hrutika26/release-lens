from datetime import datetime

from pydantic import BaseModel


class ImportValidationResponse(BaseModel):
    total_records: int
    valid_records: int
    invalid_records: int


class ImportReleaseMetadataResponse(BaseModel):
    version: str
    commit_sha: str | None


class ImportEnvironmentMetadataResponse(BaseModel):
    name: str
    deployed_at: datetime | None


class ImportPreviewResponse(BaseModel):
    import_id: int
    file_name: str
    status: str

    release: ImportReleaseMetadataResponse
    environment: ImportEnvironmentMetadataResponse
    validation: ImportValidationResponse

    can_import: bool


class ImportConfirmResponse(BaseModel):
    import_id: int
    status: str
    message: str


class ImportJobStatusResponse(BaseModel):
    import_id: int
    status: str

    total_records: int
    processed_records: int
    valid_records: int
    invalid_records: int

    error_message: str | None

    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None