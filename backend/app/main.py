from __future__ import annotations

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    role: str = "Developer"


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str | None = None
    repository_url: str | None = None
    status: str = "active"


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    repository_url: str | None = None
    status: str | None = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    repository_url: str | None = None
    status: str
    owner_email: str


class ScanOut(BaseModel):
    id: int
    project_id: int
    status: str
    summary: str
    findings_count: int


class FindingRecord(BaseModel):
    id: int
    project_id: int
    file: str
    line_number: int
    rule: str
    severity: str
    description: str
    recommendation: str
    status: str = "open"


class DashboardSummary(BaseModel):
    total_projects: int
    total_scans: int
    open_vulnerabilities: int
    critical_findings: int
    risk_distribution: dict[str, int]
    recent_findings: list[FindingRecord]
