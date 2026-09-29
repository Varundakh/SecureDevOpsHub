from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, dashboard, health, projects, scans

app = FastAPI(title="SecureDevOpsHub", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(scans.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(health.router, prefix="/api")


@app.get("/")
def read_root() -> dict:
    return {"message": "SecureDevOpsHub API is running"}
