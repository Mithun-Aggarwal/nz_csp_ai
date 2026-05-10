"""SQLite helper functions for the prototype.

This module provides a small database boundary so the UI does not directly own
connection details. The local database is stored in ``database/app.db`` by
configuration so behaviour is predictable on a Mac and on Streamlit Cloud.
"""

import sqlite3
from pathlib import Path
from typing import Dict, Iterable, Union

from config.roles import ROLE_CSP_ADMIN, ROLE_GSK_LIMITED_VIEWER, ROLE_HCP, ROLE_PHARMACIST
from config.settings import DATABASE_PATH, SCHEMA_PATH

PathLike = Union[str, Path]


class DatabaseInitialisationError(RuntimeError):
    """Raised when the local SQLite schema cannot be initialised."""


DEMO_USERS = [
    {
        "display_name": "Dr Amelia Smith",
        "email": "amelia.smith@example.test",
        "role": ROLE_HCP,
        "organisation": "Auckland Private Haematology",
    },
    {
        "display_name": "Priya Patel",
        "email": "priya.patel@example.test",
        "role": ROLE_PHARMACIST,
        "organisation": "Auckland Oncology Pharmacy",
    },
    {
        "display_name": "Alex Morgan",
        "email": "alex.morgan@example.test",
        "role": ROLE_CSP_ADMIN,
        "organisation": "CSP Vendor Admin",
    },
    {
        "display_name": "GSK Programme Viewer",
        "email": "gsk.viewer@example.test",
        "role": ROLE_GSK_LIMITED_VIEWER,
        "organisation": "GSK NZ",
    },
]


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


def _column_exists(connection: sqlite3.Connection, table_name: str, column_name: str) -> bool:
    """Return whether a SQLite table already has a column."""

    columns = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(row["name"] == column_name for row in columns)


def _add_columns_if_missing(
    connection: sqlite3.Connection,
    table_name: str,
    columns: Dict[str, str],
) -> None:
    """Add simple nullable/default columns for local prototype migrations."""

    for column_name, column_sql in columns.items():
        if not _column_exists(connection, table_name, column_name):
            connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_sql}")


def _run_lightweight_migrations(connection: sqlite3.Connection) -> None:
    """Bring existing Step 1/2 local databases up to the Step 3 draft schema."""

    _add_columns_if_missing(
        connection,
        "users",
        {
            "role": "role TEXT",
            "organisation": "organisation TEXT",
            "is_active": "is_active INTEGER NOT NULL DEFAULT 1",
            "updated_at": "updated_at TEXT",
        },
    )
    user_columns = {row["name"] for row in connection.execute("PRAGMA table_info(users)").fetchall()}
    if "role_key" in user_columns:
        connection.execute(
            "UPDATE users SET role = COALESCE(role, role_key, 'HCP') WHERE role IS NULL"
        )
    else:
        connection.execute("UPDATE users SET role = COALESCE(role, 'HCP') WHERE role IS NULL")

    if "organisation_name" in user_columns:
        connection.execute(
            "UPDATE users SET organisation = COALESCE(organisation, organisation_name) "
            "WHERE organisation IS NULL"
        )

    _add_columns_if_missing(
        connection,
        "patients",
        {
            "site_name": "site_name TEXT",
            "treating_hcp_name": "treating_hcp_name TEXT",
            "created_by_user_id": "created_by_user_id INTEGER",
            "created_by_role": "created_by_role TEXT",
        },
    )

    _add_columns_if_missing(
        connection,
        "audit_log",
        {
            "performed_by_user_id": "performed_by_user_id INTEGER",
            "performed_by_display_name": "performed_by_display_name TEXT",
            "performed_by_role": "performed_by_role TEXT",
            "details": "details TEXT",
        },
    )

    _add_columns_if_missing(
        connection,
        "notifications",
        {
            "event_type": "event_type TEXT",
            "recipient_role": "recipient_role TEXT",
            "recipient_email": "recipient_email TEXT",
            "message": "message TEXT",
            "status": "status TEXT NOT NULL DEFAULT 'simulated'",
        },
    )


def seed_demo_users(db_path: PathLike = DATABASE_PATH) -> None:
    """Ensure the four fake Step 3 demo users exist exactly once by email."""

    with get_connection(db_path) as connection:
        user_columns = {row["name"] for row in connection.execute("PRAGMA table_info(users)").fetchall()}
        for user in DEMO_USERS:
            existing = connection.execute(
                "SELECT id FROM users WHERE email = ?", (user["email"],)
            ).fetchone()
            if existing:
                connection.execute(
                    """
                    UPDATE users
                    SET display_name = ?,
                        role = ?,
                        organisation = ?,
                        is_active = 1
                    WHERE email = ?
                    """,
                    (
                        user["display_name"],
                        user["role"],
                        user["organisation"],
                        user["email"],
                    ),
                )
                if "role_key" in user_columns:
                    connection.execute(
                        "UPDATE users SET role_key = ? WHERE email = ?",
                        (user["role"], user["email"]),
                    )
                if "organisation_name" in user_columns:
                    connection.execute(
                        "UPDATE users SET organisation_name = ? WHERE email = ?",
                        (user["organisation"], user["email"]),
                    )
                continue

            insert_values = {
                "display_name": user["display_name"],
                "email": user["email"],
                "role": user["role"],
                "organisation": user["organisation"],
                "is_active": 1,
            }
            if "role_key" in user_columns:
                insert_values["role_key"] = user["role"]
            if "organisation_name" in user_columns:
                insert_values["organisation_name"] = user["organisation"]
            if "approval_status" in user_columns:
                insert_values["approval_status"] = "approved"

            columns = [column for column in insert_values if column in user_columns]
            placeholders = ", ".join(["?" for _ in columns])
            connection.execute(
                "INSERT INTO users (%s) VALUES (%s)" % (", ".join(columns), placeholders),
                tuple(insert_values[column] for column in columns),
            )


def initialise_database(
    db_path: PathLike = DATABASE_PATH,
    schema_path: PathLike = SCHEMA_PATH,
) -> None:
    """Create prototype tables, run small local migrations, and seed demo users."""

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
            _run_lightweight_migrations(connection)
        seed_demo_users(database_path)
    except sqlite3.Error as exc:
        raise DatabaseInitialisationError(
            f"Unable to initialise SQLite database at {database_path}: {exc}"
        ) from exc


def rows_to_dicts(rows: Iterable[sqlite3.Row]) -> list:
    """Convert SQLite rows to plain dictionaries for Streamlit tables."""

    return [dict(row) for row in rows]
