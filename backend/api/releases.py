from fastapi import APIRouter, Depends, HTTPException, status

from db.dependencies import get_services
from schemas.release import ReleaseSummaryResponse
from services.services import Services


router = APIRouter(
    prefix="/projects/{project_id}/releases",
    tags=["Releases"],
)


@router.get(
    "",
    response_model=list[ReleaseSummaryResponse],
)
async def get_project_releases(
    project_id: int,
    services: Services = Depends(get_services),
):
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