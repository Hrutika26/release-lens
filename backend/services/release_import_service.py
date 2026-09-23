from datetime import datetime
import json
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from pydantic import ValidationError

from models.api_request import ApiRequest
from db.repositories import Repositories
from schemas.api_request import ApiRequestImport
from schemas.import_job import ImportEnvironmentMetadataResponse, ImportPreviewResponse, ImportReleaseMetadataResponse, ImportValidationResponse
from schemas.release_import import ReleaseImportMetadata


IMPORT_DIRECTORY = Path("data/imports")


class ReleaseImportService:
    def __init__(self, repositories: Repositories):
        self.project_repository = repositories.project
        self.import_job_repository = repositories.import_job
        self.release_repository = repositories.release
        self.release_environment_repository = repositories.release_environment
        self.api_request_repository = repositories.api_request
        self.endpoint_metric_repository = repositories.endpoint_metric

    async def preview_import(self, project_id: int, file: UploadFile) -> ImportPreviewResponse:

        project = await self.project_repository.find_by_id(project_id)

        if project is None:
            raise ValueError("Project not found")

        file_path = await self._save_file(file)

        metadata, total_records, valid_records, invalid_records = (
            self._validate_file(file_path)
        )

        import_job = await self.import_job_repository.create(
            project_id=project_id,
            file_name=file.filename or file_path.name,
            file_path=str(file_path),
            version=metadata.version,
            environment=metadata.environment,
            commit_sha=metadata.commit_sha,
            deployed_at=metadata.deployed_at,
            status="PENDING_CONFIRMATION",
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
        )

        return ImportPreviewResponse(
            import_id=import_job.id,
            file_name=import_job.file_name,
            status=import_job.status,

            release=ImportReleaseMetadataResponse(
                version=metadata.version,
                commit_sha=metadata.commit_sha,
            ),

            environment=ImportEnvironmentMetadataResponse(
                name=metadata.environment,
                deployed_at=metadata.deployed_at,
            ),

            validation=ImportValidationResponse(
                total_records=total_records,
                valid_records=valid_records,
                invalid_records=invalid_records,
            ),

            can_import=valid_records > 0,
        )

    async def _save_file(self, file: UploadFile) -> Path:
        IMPORT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        original_name = (
            Path(file.filename).name
            if file.filename
            else "release.ndjson"
        )

        file_path = (
            IMPORT_DIRECTORY
            / f"{uuid4()}_{original_name}"
        )

        with file_path.open("wb") as destination:
            while chunk := await file.read(1024 * 1024):
                destination.write(chunk)

        return file_path

    def _validate_file(self, file_path: Path) -> tuple[ReleaseImportMetadata, int, int, int]:
        total_records = 0
        valid_records = 0
        invalid_records = 0

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            metadata_line = file.readline()

            if not metadata_line:
                raise ValueError(
                    "NDJSON file is empty"
                )

            try:
                metadata_json = json.loads(
                    metadata_line
                )

                metadata = (
                    ReleaseImportMetadata
                    .model_validate(metadata_json)
                )

            except (
                json.JSONDecodeError,
                ValidationError,
            ) as error:
                raise ValueError(
                    "Invalid release metadata"
                ) from error

            for line in file:
                line = line.strip()

                if not line:
                    continue

                total_records += 1

                try:
                    request_json = json.loads(line)

                    ApiRequestImport.model_validate(
                        request_json
                    )

                    valid_records += 1

                except (
                    json.JSONDecodeError,
                    ValidationError,
                ):
                    invalid_records += 1

        return (
            metadata,
            total_records,
            valid_records,
            invalid_records,
        )

    async def confirm_import(self, project_id: int, import_id: int) -> None:
        import_job = await self.import_job_repository.find_by_id(import_id)
        if import_job is None:
            raise ValueError("Import job not found")

        if import_job.project_id != project_id:
            raise ValueError("Import job does not belong to this project")

        if import_job.status != "PENDING_CONFIRMATION":
            raise ValueError(
                f"Import cannot be confirmed with status "
                f"{import_job.status}"
            )

        await self.import_job_repository.mark_processing(import_id)

        try:
            release = await self.release_repository.find_by_project_and_version(project_id, import_job.version)

            if release is None:
                release = await self.release_repository.create(
                    project_id=project_id,
                    version=import_job.version,
                    commit_sha=import_job.commit_sha,
                )

            release_environment = (
                await self.release_environment_repository
                .find_by_release_and_environment(
                    release.id,
                    import_job.environment,
                )
            )

            if release_environment is None:
                release_environment = (
                    await self.release_environment_repository.create(
                        release_id=release.id,
                        environment=import_job.environment,
                        deployed_at=import_job.deployed_at,
                    )
                )

            processed_records = await self._process_import_file(
                import_job.file_path,
                release_environment.id,
                import_id,
            )

            await (
                self.endpoint_metric_repository
                .recalculate_for_release_environment(
                    release_environment.id
                )
            )

            await self.import_job_repository.mark_completed(
                import_id=import_id,
                processed_records=processed_records,
            )

        except Exception as error:
            await self.import_job_repository.mark_failed(
                import_id=import_id,
                error_message=str(error),
            )

            raise

    async def _process_import_file( self, file_path: str, release_environment_id: int, import_id: int) -> int:
        batch_size = 1000

        batch = []
        processed_records = 0

        path = Path(file_path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            # Skip metadata line
            file.readline()

            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    request_json = json.loads(line)

                    request_data = (
                        ApiRequestImport
                        .model_validate(request_json)
                    )

                except (
                    json.JSONDecodeError,
                    ValidationError,
                ):
                    continue

                batch.append(
                    ApiRequest(
                        id=0,
                        release_environment_id=release_environment_id,
                        request_id=request_data.request_id,
                        timestamp=request_data.timestamp,
                        endpoint=request_data.endpoint,
                        method=request_data.method,
                        status_code=request_data.status_code,
                        response_time_ms=request_data.response_time_ms,
                        created_at=datetime.now(),
                    )
                )

                if len(batch) >= batch_size:
                    await self.api_request_repository.batch_insert(
                        release_environment_id,
                        batch,
                    )

                    processed_records += len(batch)

                    await (
                        self.import_job_repository
                        .update_processed_records(
                            import_id,
                            processed_records,
                        )
                    )

                    batch.clear()

            if batch:
                await self.api_request_repository.batch_insert(
                    release_environment_id,
                    batch,
                )

                processed_records += len(batch)

                await (
                    self.import_job_repository
                    .update_processed_records(
                        import_id,
                        processed_records,
                    )
                )

        return processed_records

    async def get_import_status(self, project_id: int, import_id: int):
        import_job = await self.import_job_repository.find_by_id(import_id)
        if import_job is None:
            return None

        if import_job.project_id != project_id:
            return None

        return import_job
