from __future__ import annotations

from app.scanners.engine import SecurityEngine


class RiskAnalyzer:
    def __init__(self) -> None:
        self.engine = SecurityEngine()

    def analyze(self, project: dict) -> list[dict]:
        return self.engine.scan_repository(project)
