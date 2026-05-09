"""Notification simulation service.

No real email is sent in Step 1. Future implementation should persist
notifications, apply templates, enforce role-based content, and integrate with
an approved email provider if required.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class NotificationDraft:
    """Represents a simulated notification event."""

    recipient_role: str
    subject: str
    message: str
    created_at: datetime


def build_milestone_notification(recipient_role: str, milestone: str) -> NotificationDraft:
    """Create a non-sensitive placeholder milestone notification."""

    return NotificationDraft(
        recipient_role=recipient_role,
        subject=f"CSP milestone: {milestone}",
        message="Prototype notification only. Log in to view role-appropriate details.",
        created_at=datetime.now(timezone.utc),
    )
