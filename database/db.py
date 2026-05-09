"""SQLite helper functions for the prototype.

This module provides a tiny database boundary so the UI does not directly own
connection details. It is intentionally minimal for Step 1.
"""

import sqlite3
from pathlib import Path

from config.settings import DATABASE_PATH, SCHEMA_PATH


def get_connection(db_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Return a SQLite connection for the local prototype database."""

    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database(db_path: Path = DATABASE_PATH, schema_path: Path = SCHEMA_PATH) -> None:
    """Create prototype tables if they do not already exist."""

    with get_connection(db_path) as connection:
        connection.executescript(schema_path.read_text(encoding="utf-8"))
