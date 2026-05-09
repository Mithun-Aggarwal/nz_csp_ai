"""User model placeholders for the prototype."""

from dataclasses import dataclass


@dataclass
class User:
    """Minimal user representation for Step 1 discussions."""

    email: str
    display_name: str
    role_key: str
    approval_status: str = "pending"
