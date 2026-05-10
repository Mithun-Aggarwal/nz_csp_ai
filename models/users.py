"""User model for fake Step 3 demo users."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Minimal fake user representation for the mock role-based prototype."""

    id: Optional[int]
    email: str
    display_name: str
    role: str
    organisation: str
    is_active: bool = True
