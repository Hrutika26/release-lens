from fastapi import APIRouter, Depends, HTTPException, status

from db.dependencies import get_services
from schemas.release import ReleaseDetailResponse, ReleaseSummaryResponse
from services.services import Services
from schemas.endpoint_metric import EndpointMetricResponse
from schemas.release_comparison import ReleaseEnvironmentComparisonResponse

router = APIRouter(
    prefix="/projects/{project_id}/releases",
    tags=["Releases"],
)


@router.get(
    "",
    response_model=list[ReleaseSummaryResponse],
)
async def get_project_releases(project_id: int, services: Services = Depends(get_services)):
    project = await services.project.get_project(
        project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return await services.release.get_releases_by_project(
        project_id
    )

@router.get(
    "/compare",
    response_model=ReleaseEnvironmentComparisonResponse,
)
async def compare_releases(
    project_id: int,
    base_environment_id: int,
    target_environment_id: int,
    services: Services = Depends(get_services),
):
    try:
        return await services.release_comparison.compare(
            project_id=project_id,
            base_environment_id=base_environment_id,
            target_environment_id=target_environment_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

@router.get(
    "/{release_id}",
    response_model=ReleaseDetailResponse,
)
async def get_release(
    project_id: int,
    release_id: int,
    services: Services = Depends(get_services),
):
    release = await services.release.get_release_detail(
        project_id=project_id,
        release_id=release_id,
    )

    if release is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release not found.",
        )

    return release

@router.get(
    "/{release_id}/environments/{environment_id}/metrics",
    response_model=list[EndpointMetricResponse],
)
async def get_environment_metrics(
    project_id: int,
    release_id: int,
    environment_id: int,
    services: Services = Depends(get_services),
):
    metrics = (
        await services.release
        .get_environment_metrics(
            project_id=project_id,
            release_id=release_id,
            environment_id=environment_id,
        )
    )

    if metrics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Release environment not found.",
        )

    return metrics

