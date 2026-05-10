"""Central role and permission definitions for the prototype portal.

The Step 3 portal uses these constants for simple mock access control. This is
not production authentication or authorisation.
"""

from dataclasses import dataclass
from typing import Dict, List, Set


@dataclass(frozen=True)
class Role:
    """Describes a prototype portal role."""

    key: str
    display_name: str
    description: str


ROLE_HCP = "HCP"
ROLE_PHARMACIST = "Pharmacist"
ROLE_CSP_ADMIN = "CSP Admin"
ROLE_GSK_LIMITED_VIEWER = "GSK Limited Viewer"

PERMISSION_CREATE_PROGRAMME_RECORD = "can_create_programme_record"
PERMISSION_VIEW_OWN_PROGRAMME_RECORDS = "can_view_own_programme_records"
PERMISSION_VIEW_ALL_PROGRAMME_RECORDS = "can_view_all_programme_records"
PERMISSION_VIEW_LIMITED_DASHBOARD = "can_view_limited_dashboard"
PERMISSION_VIEW_NOTIFICATIONS = "can_view_notifications"
PERMISSION_VIEW_AUDIT_LOG = "can_view_audit_log"
PERMISSION_ACCESS_CSP_ADMIN = "can_access_csp_admin"
PERMISSION_PREPARE_PROGRAMME_RECORD = "can_prepare_programme_record"
PERMISSION_SUBMIT_PROGRAMME_RECORD = "can_submit_programme_record"

HCP = Role(
    key=ROLE_HCP,
    display_name=ROLE_HCP,
    description="Private haematologist role for basic demo programme record creation.",
)
PHARMACIST = Role(
    key=ROLE_PHARMACIST,
    display_name=ROLE_PHARMACIST,
    description="Private pharmacist role for basic demo programme record preparation.",
)
CSP_ADMIN = Role(
    key=ROLE_CSP_ADMIN,
    display_name=ROLE_CSP_ADMIN,
    description="Programme administrator role with broad prototype oversight.",
)
GSK_LIMITED_VIEWER = Role(
    key=ROLE_GSK_LIMITED_VIEWER,
    display_name=ROLE_GSK_LIMITED_VIEWER,
    description="Restricted non-sensitive dashboard-only programme view.",
)

ROLES = [HCP, PHARMACIST, CSP_ADMIN, GSK_LIMITED_VIEWER]
ROLE_BY_KEY = {role.key: role for role in ROLES}

ROLE_PERMISSIONS: Dict[str, Set[str]] = {
    ROLE_HCP: {
        PERMISSION_CREATE_PROGRAMME_RECORD,
        PERMISSION_VIEW_OWN_PROGRAMME_RECORDS,
        PERMISSION_SUBMIT_PROGRAMME_RECORD,
    },
    ROLE_PHARMACIST: {
        PERMISSION_CREATE_PROGRAMME_RECORD,
        PERMISSION_PREPARE_PROGRAMME_RECORD,
        PERMISSION_VIEW_OWN_PROGRAMME_RECORDS,
    },
    ROLE_CSP_ADMIN: {
        PERMISSION_CREATE_PROGRAMME_RECORD,
        PERMISSION_VIEW_ALL_PROGRAMME_RECORDS,
        PERMISSION_VIEW_NOTIFICATIONS,
        PERMISSION_VIEW_AUDIT_LOG,
        PERMISSION_ACCESS_CSP_ADMIN,
        PERMISSION_SUBMIT_PROGRAMME_RECORD,
        PERMISSION_PREPARE_PROGRAMME_RECORD,
    },
    ROLE_GSK_LIMITED_VIEWER: {
        PERMISSION_VIEW_LIMITED_DASHBOARD,
    },
}


def role_options() -> List[str]:
    """Return role keys for legacy mock role selection controls."""

    return [role.key for role in ROLES]


def get_role_label(role_key: str) -> str:
    """Return a display label for a role key."""

    return ROLE_BY_KEY.get(role_key, HCP).display_name


def get_role_permissions(role: str) -> List[str]:
    """Return the sorted permission names granted to a role."""

    return sorted(ROLE_PERMISSIONS.get(role, set()))


def role_has_permission(role: str, permission: str) -> bool:
    """Return whether the role has the requested permission."""

    return permission in ROLE_PERMISSIONS.get(role, set())
