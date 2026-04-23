from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, URL, make_url
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_api_settings

_ENGINE_CACHE: dict[str, Engine] = {}
_SESSION_FACTORY_CACHE: dict[str, sessionmaker[Session]] = {}


def _resolve_database_url(database_url: str | None = None) -> str:
    return database_url or get_api_settings().database_url


def _prepare_sqlite_directory(database_url: str) -> None:
    url = make_url(database_url)
    if not isinstance(url, URL):
        return
    if not url.drivername.startswith("sqlite"):
        return
    if not url.database or url.database == ":memory:":
        return

    database_path = Path(url.database)
    if not database_path.is_absolute():
        database_path = Path.cwd() / database_path
    database_path.parent.mkdir(parents=True, exist_ok=True)


def get_engine(database_url: str | None = None) -> Engine:
    resolved_database_url = _resolve_database_url(database_url)
    if resolved_database_url not in _ENGINE_CACHE:
        _prepare_sqlite_directory(resolved_database_url)
        _ENGINE_CACHE[resolved_database_url] = create_engine(resolved_database_url, future=True)
    return _ENGINE_CACHE[resolved_database_url]


def get_session_factory(database_url: str | None = None) -> sessionmaker[Session]:
    resolved_database_url = _resolve_database_url(database_url)
    if resolved_database_url not in _SESSION_FACTORY_CACHE:
        _SESSION_FACTORY_CACHE[resolved_database_url] = sessionmaker(
            bind=get_engine(resolved_database_url),
            autoflush=False,
            autocommit=False,
            future=True,
        )
    return _SESSION_FACTORY_CACHE[resolved_database_url]


def get_db_session(database_url: str | None = None) -> Session:
    return get_session_factory(database_url)()


def reset_db_session_state(database_url: str | None = None) -> None:
    if database_url is not None:
        resolved_database_url = _resolve_database_url(database_url)
        engine = _ENGINE_CACHE.pop(resolved_database_url, None)
        _SESSION_FACTORY_CACHE.pop(resolved_database_url, None)
        if engine is not None:
            engine.dispose()
        return

    engines = list(_ENGINE_CACHE.values())
    _ENGINE_CACHE.clear()
    _SESSION_FACTORY_CACHE.clear()
    for engine in engines:
        engine.dispose()
