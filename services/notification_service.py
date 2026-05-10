"""SQLite-backed simulated notification service for Step 3.

No real email is sent. Notifications are inserted into SQLite so CSP Admin can
see that a prototype event would have occurred.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from config.roles import ROLE_CSP_ADMIN
from database.db import get_connection, rows_to_dicts

CSP_ADMIN_DEMO_EMAIL = "alex.morgan@example.test"


@dataclass
class NotificationDraft:
    """Represents a simulated notification event."""

    recipient_role: str
    subject: str
    message: str
    created_at: datetime


@dataclass
class NotificationRecord:
    """Represents a persisted simulated notification."""

    id: int
    event_type: Optional[str]
    recipient_role: Optional[str]
    recipient_email: Optional[str]
    message: Optional[str]
    status: str
    created_at: str


def build_milestone_notification(recipient_role: str, milestone: str) -> NotificationDraft:
    """Create a non-sensitive placeholder milestone notification."""

    return NotificationDraft(
        recipient_role=recipient_role,
        subject="CSP milestone: %s" % milestone,
        message="Prototype notification only. Log in to view role-appropriate details.",
        created_at=datetime.now(timezone.utc),
    )


def create_programme_record_notification() -> int:
    """Persist a simulated CSP Admin notification for a new programme record."""

    message = "New demo programme record created and awaiting next step."
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO notifications (
                event_type,
                recipient_role,
                recipient_email,
                message,
                status,
                recipient_role_key,
                subject,
                delivery_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "programme_record_created",
                ROLE_CSP_ADMIN,
                CSP_ADMIN_DEMO_EMAIL,
                message,
                "simulated",
                ROLE_CSP_ADMIN,
                "Demo programme record created",
                "simulated",
            ),
        )
        return int(cursor.lastrowid)


def list_notifications() -> List[NotificationRecord]:
    """Return persisted simulated notifications ordered newest first."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, event_type, recipient_role, recipient_email, message, status, created_at
            FROM notifications
            ORDER BY datetime(created_at) DESC, id DESC
            """
        ).fetchall()
    return [NotificationRecord(**row) for row in rows_to_dicts(rows)]


def count_notifications() -> int:
    """Return a count of simulated notifications."""

    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) AS total FROM notifications").fetchone()
    return int(row["total"])
