from fastapi import APIRouter, Depends, File, HTTPException, UploadFile,status

from db.dependencies import get_services
from services.services import Services
from schemas.import_job import ImportConfirmResponse, ImportPreviewResponse, ImportJobStatusResponse

router = APIRouter(
    prefix="/projects/{project_id}/release-imports",
    tags=["Release Imports"],
)

@router.post("/preview", response_model=ImportPreviewResponse, status_code=status.HTTP_200_OK)
async def preview_release_import(project_id: int, file: UploadFile = File(...), services: Services = Depends(get_services)):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required.",
        )

    if not file.filename.lower().endswith(".ndjson"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only NDJSON files are supported.",
        )

    try:
        return await services.release_import.preview_import(
            project_id=project_id,
            file=file,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

@router.post("/{import_id}/confirm", response_model=ImportConfirmResponse, status_code=status.HTTP_202_ACCEPTED)
async def confirm_release_import(project_id: int, import_id: int, services: Services = Depends(get_services)):
    try:
        await services.release_import.confirm_import(
            project_id=project_id,
            import_id=import_id,
        )

        return ImportConfirmResponse(
            import_id=import_id,
            status="COMPLETED",
            message="Release import completed.",
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Release import failed.",
        ) from error

@router.get("/{import_id}", response_model=ImportJobStatusResponse)
async def get_release_import_status(project_id: int, import_id: int, services: Services = Depends(get_services)):
    import_job = await (
        services.release_import.get_import_status(
            project_id=project_id,
            import_id=import_id,
        )
    )

    if import_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Import job not found.",
        )

    return ImportJobStatusResponse(
        import_id=import_job.id,
        status=import_job.status,
        total_records=import_job.total_records,
        processed_records=import_job.processed_records,
        valid_records=import_job.valid_records,
        invalid_records=import_job.invalid_records,
        error_message=import_job.error_message,
        created_at=import_job.created_at,
        started_at=import_job.started_at,
        completed_at=import_job.completed_at,
    )