from __future__ import annotations

from typing import Any


class SecurityEngine:
    def scan_repository(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        name = str(payload.get("name", "")).lower()

        if "secret" in name:
            findings.append(
                {
                    "file": "config/settings.py",
                    "line_number": 14,
                    "rule": "secret_repository_name",
                    "severity": "MEDIUM",
                    "description": "Repository name suggests exposure of secrets or sensitive configuration.",
                    "recommendation": "Use a neutral project name and rotate any exposed credentials.",
                }
            )

        repo_url = str(payload.get("repository_url", ""))
        if repo_url and "github.com" not in repo_url:
            findings.append(
                {
                    "file": "README.md",
                    "line_number": 1,
                    "rule": "repository_url_validation",
                    "severity": "LOW",
                    "description": "The provided repository URL does not resemble a supported GitHub remote.",
                    "recommendation": "Validate the remote before running scans.",
                }
            )

        return findings
