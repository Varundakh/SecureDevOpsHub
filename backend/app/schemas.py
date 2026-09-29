from __future__ import annotations

from typing import Any

users: dict[str, dict[str, Any]] = {}
projects: dict[int, dict[str, Any]] = {}
scans: dict[int, dict[str, Any]] = {}
findings: dict[int, dict[str, Any]] = {}

_next_user_id = 1
_next_project_id = 1
_next_scan_id = 1
_next_finding_id = 1


def next_id(kind: str) -> int:
    global _next_user_id, _next_project_id, _next_scan_id, _next_finding_id
    if kind == "user":
        value = _next_user_id
        _next_user_id += 1
        return value
    if kind == "project":
        value = _next_project_id
        _next_project_id += 1
        return value
    if kind == "scan":
        value = _next_scan_id
        _next_scan_id += 1
        return value
    value = _next_finding_id
    _next_finding_id += 1
    return value


def get_user_by_email(email: str) -> dict[str, Any] | None:
    return users.get(email)


def create_user(email: str, hashed_password: str, role: str) -> dict[str, Any]:
    user = {"id": next_id("user"), "email": email, "hashed_password": hashed_password, "role": role}
    users[email] = user
    return user


def create_project(name: str, description: str | None, repository_url: str | None, owner_email: str) -> dict[str, Any]:
    project = {
        "id": next_id("project"),
        "name": name,
        "description": description,
        "repository_url": repository_url,
        "status": "active",
        "owner_email": owner_email,
    }
    projects[project["id"]] = project
    return project


def get_project(project_id: int) -> dict[str, Any] | None:
    return projects.get(project_id)


def list_projects() -> list[dict[str, Any]]:
    return list(projects.values())


def delete_project(project_id: int) -> None:
    projects.pop(project_id, None)


def create_scan(project_id: int, status: str = "running", summary: str = "Queued") -> dict[str, Any]:
    scan = {"id": next_id("scan"), "project_id": project_id, "status": status, "summary": summary, "findings_count": 0}
    scans[scan["id"]] = scan
    return scan


def list_scans_for_project(project_id: int) -> list[dict[str, Any]]:
    return [scan for scan in scans.values() if scan["project_id"] == project_id]


def create_finding(project_id: int, file: str, line_number: int, rule: str, severity: str, description: str, recommendation: str) -> dict[str, Any]:
    row = {
        "id": next_id("finding"),
        "project_id": project_id,
        "file": file,
        "line_number": line_number,
        "rule": rule,
        "severity": severity,
        "description": description,
        "recommendation": recommendation,
        "status": "open",
    }
    findings[row["id"]] = row
    return row


def list_findings() -> list[dict[str, Any]]:
    return list(findings.values())


def get_dashboard_summary() -> dict[str, Any]:
    total_projects = len(projects)
    total_scans = len(scans)
    open_vulnerabilities = sum(1 for item in findings.values() if item["status"] == "open")
    critical_findings = sum(1 for item in findings.values() if item["severity"] == "CRITICAL")
    risk_distribution = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
    for item in findings.values():
        risk_distribution[item["severity"]] = risk_distribution.get(item["severity"], 0) + 1
    recent_findings = sorted(findings.values(), key=lambda item: item["id"], reverse=True)[:5]
    return {
        "total_projects": total_projects,
        "total_scans": total_scans,
        "open_vulnerabilities": open_vulnerabilities,
        "critical_findings": critical_findings,
        "risk_distribution": risk_distribution,
        "recent_findings": recent_findings,
    }
