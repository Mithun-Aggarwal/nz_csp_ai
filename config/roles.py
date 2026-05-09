"""Central role definitions for the Blenrep NZ CSP Portal prototype.

These roles are placeholders for Step 1. They are intentionally simple and
must be replaced by a production access-control model before real use.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Role:
    """Describes a prototype portal role."""

    key: str
    display_name: str
    description: str


HCP = Role(
    key="hcp",
    display_name="HCP",
    description="Private haematologist role for allocated patient workflow.",
)
PHARMACIST = Role(
    key="pharmacist",
    display_name="Pharmacist",
    description="Private pharmacist role for data entry and reorder support.",
)
CSP_ADMIN = Role(
    key="csp_admin",
    display_name="CSP Admin",
    description="Programme administrator role with broad operational oversight.",
)
GSK_LIMITED_VIEWER = Role(
    key="gsk_limited_viewer",
    display_name="GSK Limited Viewer",
    description="Restricted non-sensitive dashboard-only programme view.",
)

ROLES = [HCP, PHARMACIST, CSP_ADMIN, GSK_LIMITED_VIEWER]
ROLE_BY_KEY = {role.key: role for role in ROLES}


def role_options() -> list[str]:
    """Return role keys for mock role selection controls."""

    return [role.key for role in ROLES]


def get_role_label(role_key: str) -> str:
    """Return a display label for a role key."""

    return ROLE_BY_KEY.get(role_key, HCP).display_name
