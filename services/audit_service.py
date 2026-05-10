"""SQLite-backed audit trail helpers for Step 3."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from database.db import get_connection, rows_to_dicts


@dataclass
class AuditEvent:
    """Represents a persisted audit event."""

    id: int
    event_action: str
    entity_type: str
    entity_id: Optional[str]
    performed_by_user_id: Optional[int]
    performed_by_display_name: Optional[str]
    performed_by_role: Optional[str]
    details: Optional[str]
    created_at: str


def create_audit_event(
    event_action: str,
    entity_type: str,
    entity_id: Optional[str],
    performed_by_user: Dict[str, Any],
    details: str,
) -> int:
    """Persist a simple audit event and return its id."""

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO audit_log (
                event_action,
                entity_type,
                entity_id,
                performed_by_user_id,
                performed_by_display_name,
                performed_by_role,
                details,
                actor_user_id,
                actor_role_key,
                details_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_action,
                entity_type,
                entity_id,
                performed_by_user.get("id"),
                performed_by_user.get("display_name"),
                performed_by_user.get("role"),
                details,
                performed_by_user.get("id"),
                performed_by_user.get("role"),
                details,
            ),
        )
        return int(cursor.lastrowid)


def list_audit_events() -> List[AuditEvent]:
    """Return persisted audit events ordered newest first."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                event_action,
                entity_type,
                entity_id,
                performed_by_user_id,
                performed_by_display_name,
                performed_by_role,
                details,
                created_at
            FROM audit_log
            ORDER BY datetime(created_at) DESC, id DESC
            """
        ).fetchall()
    return [AuditEvent(**row) for row in rows_to_dicts(rows)]
