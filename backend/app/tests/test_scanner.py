from __future__ import annotations

from app.scanners.engine import SecurityEngine


def test_engine_generates_findings() -> None:
    engine = SecurityEngine()
    findings = engine.scan_repository({"name": "secret-project", "repository_url": "https://github.com/example/demo"})
    assert findings
    assert findings[0]["severity"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
