from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import get_current_user, require_roles, security
from app.schemas import (
    ProjectCreate,
    ProjectOut,
    ScanOut,
    create_project,
    create_scan,
    delete_project,
    get_project,
    list_projects,
    list_scans_for_project,
)

router = APIRouter(prefix="/projects", tags=["projects"])


def ensure_project_access(current_user: dict, project_id: int) -> dict:
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if current_user["role"] == "Admin":
        return project

    if project["owner_email"] != current_user["email"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this project",
        )

    return project


@router.get("", response_model=list[ProjectOut])
def list_all_projects(credentials: HTTPAuthorizationCredentials = Depends(security)) -> list[ProjectOut]:
    current_user = get_current_user(credentials)
    visible_projects = list_projects()

    if current_user["role"] != "Admin":
        visible_projects = [p for p in visible_projects if p["owner_email"] == current_user["email"]]

    return [
        ProjectOut(
            id=item["id"],
            name=item["name"],
            description=item["description"],
            repository_url=item["repository_url"],
            status=item["status"],
            owner_email=item["owner_email"],
        )
        for item in visible_projects
    ]


@router.post("", response_model=ProjectOut)
def create_new_project(
    payload: ProjectCreate,
    current_user: dict = Depends(require_roles(["Admin", "Developer"])),
) -> ProjectOut:
    project = create_project(payload.name, payload.description, payload.repository_url, current_user["email"])
    return ProjectOut(
        id=project["id"],
        name=project["name"],
        description=project["description"],
        repository_url=project["repository_url"],
        status=project["status"],
        owner_email=project["owner_email"],
    )


@router.get("/{project_id}", response_model=ProjectOut)
def get_project_by_id(
    project_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ProjectOut:
    current_user = get_current_user(credentials)
    project = ensure_project_access(current_user, project_id)
    return ProjectOut(
        id=project["id"],
        name=project["name"],
        description=project["description"],
        repository_url=project["repository_url"],
        status=project["status"],
        owner_email=project["owner_email"],
    )


@router.delete("/{project_id}")
def delete_project_by_id(
    project_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    current_user = get_current_user(credentials)
    if current_user["role"] != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    delete_project(project_id)
    return {"deleted": True, "project_id": project_id, "user": current_user["email"]}


@router.post("/{project_id}/scan", response_model=ScanOut)
def trigger_scan(
    project_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> ScanOut:
    current_user = get_current_user(credentials)
    ensure_project_access(current_user, project_id)

    if current_user["role"] not in {"Admin", "Developer"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    scan = create_scan(project_id, status="completed", summary="Scan completed successfully")
    return ScanOut(
        id=scan["id"],
        project_id=scan["project_id"],
        status=scan["status"],
        summary=scan["summary"],
        findings_count=scan["findings_count"],
    )


@router.get("/{project_id}/scans", response_model=list[ScanOut])
def list_scans(
    project_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> list[ScanOut]:
    current_user = get_current_user(credentials)
    ensure_project_access(current_user, project_id)

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
