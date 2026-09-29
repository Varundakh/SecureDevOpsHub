from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import get_current_user, security
from app.models import create_project, create_scan, delete_project, get_project, list_projects, list_scans_for_project
from app.schemas import ProjectCreate, ProjectOut, ScanOut

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
def list_all_projects() -> list[ProjectOut]:
    return [
        ProjectOut(
            id=item["id"],
            name=item["name"],
            description=item["description"],
            repository_url=item["repository_url"],
            status=item["status"],
            owner_email=item["owner_email"],
        )
        for item in list_projects()
    ]


@router.post("", response_model=ProjectOut)
def create_new_project(payload: ProjectCreate, credentials: HTTPAuthorizationCredentials = Depends(security)) -> ProjectOut:
    owner = get_current_user(credentials)
    project = create_project(payload.name, payload.description, payload.repository_url, owner["email"])
    return ProjectOut(
        id=project["id"],
        name=project["name"],
        description=project["description"],
        repository_url=project["repository_url"],
        status=project["status"],
        owner_email=project["owner_email"],
    )


@router.get("/{project_id}", response_model=ProjectOut)
def get_project_by_id(project_id: int) -> ProjectOut:
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return ProjectOut(
        id=project["id"],
        name=project["name"],
        description=project["description"],
        repository_url=project["repository_url"],
        status=project["status"],
        owner_email=project["owner_email"],
    )


@router.delete("/{project_id}")
def delete_project_by_id(project_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    user = get_current_user(credentials)
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    delete_project(project_id)
    return {"deleted": True, "project_id": project_id, "user": user["email"]}


@router.post("/{project_id}/scan", response_model=ScanOut)
def trigger_scan(project_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)) -> ScanOut:
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    _ = get_current_user(credentials)
    scan = create_scan(project_id, status="completed", summary="Scan completed successfully")
    return ScanOut(
        id=scan["id"],
        project_id=scan["project_id"],
        status=scan["status"],
        summary=scan["summary"],
        findings_count=scan["findings_count"],
    )


@router.get("/{project_id}/scans", response_model=list[ScanOut])
def list_scans(project_id: int) -> list[ScanOut]:
    return [
        ScanOut(
            id=scan["id"],
            project_id=scan["project_id"],
            status=scan["status"],
            summary=scan["summary"],
            findings_count=scan["findings_count"],
        )
        for scan in list_scans_for_project(project_id)
    ]
