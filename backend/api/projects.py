from fastapi import APIRouter, Depends, HTTPException, status

from db.dependencies import get_services
from schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from services.services import Services


router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate, services: Services = Depends(get_services)):
    return await services.project.create_project(data)

@router.get("", response_model=list[ProjectResponse])
async def get_projects(services: Services = Depends(get_services)):
    return await services.project.get_projects()

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, services: Services = Depends(get_services)):
    project = await services.project.get_project(project_id)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, data: ProjectUpdate, services: Services = Depends(get_services)):
    project = await services.project.update_project(project_id, data)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project