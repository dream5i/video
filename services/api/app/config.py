from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ApiSettings:
    repository_backend: str
    database_url: str


def get_api_settings() -> ApiSettings:
    database_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or "sqlite+pysqlite:///./.data/new_project.db"
    )

    return ApiSettings(
        repository_backend=os.getenv("NEW_PROJECT_REPOSITORY_BACKEND", "database"),
        database_url=database_url,
    )
