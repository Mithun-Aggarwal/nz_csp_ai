"""Audit trail placeholder service.

The production version should write immutable-style audit events for key user,
patient, workflow, notification, and administrative actions.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class AuditEvent:
    """Represents a draft audit event."""

    actor: str
    action: str
    entity_type: str
    entity_id: str | None
    created_at: datetime


def create_audit_event(actor: str, action: str, entity_type: str, entity_id: str | None = None) -> AuditEvent:
    """Build an audit event object without persisting it yet."""

    return AuditEvent(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        created_at=datetime.now(timezone.utc),
    )
