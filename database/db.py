"""SQLite helper functions for the prototype.

This module provides a small database boundary so the UI does not directly own
connection details. The local database is stored in ``database/app.db`` by
configuration so behaviour is predictable on a Mac and on Streamlit Cloud.
"""

import sqlite3
from pathlib import Path
from typing import Union

from config.settings import DATABASE_PATH, SCHEMA_PATH

PathLike = Union[str, Path]


class DatabaseInitialisationError(RuntimeError):
    """Raised when the local SQLite schema cannot be initialised."""


def _normalise_path(path: PathLike) -> Path:
    """Return a resolved Path without requiring the target to exist."""

    return Path(path).expanduser().resolve()


def get_connection(db_path: PathLike = DATABASE_PATH) -> sqlite3.Connection:
    """Return a SQLite connection for the local prototype database."""

    database_path = _normalise_path(db_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database(
    db_path: PathLike = DATABASE_PATH,
    schema_path: PathLike = SCHEMA_PATH,
) -> None:
    """Create prototype tables if they do not already exist.

    Schema failures are re-raised with context so local runs and Streamlit Cloud
    logs show what failed instead of crashing silently.
    """

    database_path = _normalise_path(db_path)
    schema_file = _normalise_path(schema_path)

    try:
        schema_sql = schema_file.read_text(encoding="utf-8")
    except OSError as exc:
        raise DatabaseInitialisationError(
            f"Unable to read SQLite schema file at {schema_file}."
        ) from exc

    try:
        with get_connection(database_path) as connection:
            connection.executescript(schema_sql)
    except sqlite3.Error as exc:
        raise DatabaseInitialisationError(
            f"Unable to initialise SQLite database at {database_path}: {exc}"
        ) from exc
