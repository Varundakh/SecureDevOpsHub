from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.models import create_finding, get_dashboard_summary, list_findings
from app.schemas import DashboardSummary, FindingRecord

router = APIRouter(prefix="/scans", tags=["scans"])


@router.get("/findings", response_model=list[FindingRecord])
def get_findings() -> list[FindingRecord]:
    return [
        FindingRecord(
            id=item["id"],
            project_id=item["project_id"],
            file=item["file"],
            line_number=item["line_number"],
            rule=item["rule"],
            severity=item["severity"],
            description=item["description"],
            recommendation=item["recommendation"],
            status=item["status"],
        )
        for item in list_findings()
    ]


@router.patch("/findings/{finding_id}")
def patch_finding(finding_id: int) -> dict:
    finding = next((item for item in list_findings() if item["id"] == finding_id), None)
    if not finding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    finding["status"] = "resolved"
    return {"updated": True, "finding_id": finding_id, "status": "resolved"}


@router.post("/projects/{project_id}/findings")
def add_finding(project_id: int, payload: dict) -> dict:
    finding = create_finding(
        project_id=project_id,
        file=payload["file"],
        line_number=payload["line_number"],
        rule=payload["rule"],
        severity=payload["severity"],
        description=payload["description"],
        recommendation=payload["recommendation"],
    )
    return {"created": True, "finding_id": finding["id"]}
