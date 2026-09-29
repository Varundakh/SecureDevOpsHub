from __future__ import annotations

from fastapi import APIRouter

from app.models import get_dashboard_summary
from app.schemas import DashboardSummary, FindingRecord

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary() -> DashboardSummary:
    data = get_dashboard_summary()
    return DashboardSummary(
        total_projects=data["total_projects"],
        total_scans=data["total_scans"],
        open_vulnerabilities=data["open_vulnerabilities"],
        critical_findings=data["critical_findings"],
        risk_distribution=data["risk_distribution"],
        recent_findings=[
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
            for item in data["recent_findings"]
        ],
    )
