from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class UserRecord:
    id: int
    email: str
    hashed_password: str
    role: str = "Developer"
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ProjectRecord:
    id: int
    name: str
    description: str | None
    repository_url: str | None
    status: str
    owner_email: str


@dataclass
class ScanRecord:
    id: int
    project_id: int
    status: str
    summary: str
    findings_count: int


@dataclass
class FindingRecord:
    id: int
    project_id: int
    file: str
    line_number: int
    rule: str
    severity: str
    description: str
    recommendation: str
    status: str = "open"
