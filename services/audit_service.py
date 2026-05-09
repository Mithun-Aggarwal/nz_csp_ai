"""Audit trail placeholder service.

The production version should write immutable-style audit events for key user,
patient, workflow, notification, and administrative actions.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional


@dataclass
class AuditEvent:
    """Represents a draft audit event."""

    actor: str
    action: str
    entity_type: str
    entity_id: Optional[str]
    created_at: datetime


def create_audit_event(
    actor: str,
    action: str,
    entity_type: str,
    entity_id: Optional[str] = None,
) -> AuditEvent:
    """Build an audit event object without persisting it yet."""

    return AuditEvent(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        created_at=datetime.now(timezone.utc),
    )


def list_audit_events() -> List[AuditEvent]:
    """Return available audit events for the prototype placeholder.

    Step 2 intentionally keeps audit persistence out of scope. Returning an
    empty list lets the Streamlit Audit Log page render a clear placeholder
    instead of failing when no records exist yet.
    """

    return []
