"""Mock user/session helpers for the Step 3 prototype.

This module deliberately does not implement production authentication, password
handling, MFA, SSO, or credential storage. It only stores the selected fake demo
user in Streamlit session state so pages can behave like a role-based portal.
"""

from typing import Any, Dict, List, Optional

import streamlit as st

from config.roles import HCP, ROLE_BY_KEY, get_role_label, role_has_permission, role_options
from database.db import DEMO_USERS, get_connection, initialise_database, rows_to_dicts

SESSION_USER_KEY = "current_user"
SESSION_ROLE_KEY = "mock_role_key"


def list_demo_users() -> List[Dict[str, Any]]:
    """Return active demo users from SQLite, falling back to constants if needed."""

    try:
        initialise_database()
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT id, display_name, email, role, organisation, is_active, created_at
                FROM users
                WHERE is_active = 1
                ORDER BY id
                """
            ).fetchall()
        users = rows_to_dicts(rows)
    except Exception:
        users = []

    if users:
        return users

    fallback_users = []
    for index, user in enumerate(DEMO_USERS, start=1):
        fallback = dict(user)
        fallback["id"] = index
        fallback["is_active"] = 1
        fallback_users.append(fallback)
    return fallback_users


def _find_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Find an active demo user by database id."""

    for user in list_demo_users():
        if int(user["id"]) == int(user_id):
            return user
    return None


def initialise_mock_session() -> None:
    """Ensure a default demo user exists in the Streamlit session."""

    users = list_demo_users()
    if not users:
        return

    current_user = st.session_state.get(SESSION_USER_KEY)
    if current_user and _find_user(int(current_user["id"])):
        st.session_state[SESSION_ROLE_KEY] = current_user["role"]
        return

    st.session_state[SESSION_USER_KEY] = users[0]
    st.session_state[SESSION_ROLE_KEY] = users[0]["role"]


def get_current_user() -> Optional[Dict[str, Any]]:
    """Return the currently selected fake demo user, if available."""

    initialise_mock_session()
    current_user = st.session_state.get(SESSION_USER_KEY)
    if current_user:
        return current_user
    return None


def set_current_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Store the selected fake demo user in Streamlit session state."""

    user = _find_user(user_id)
    if user:
        st.session_state[SESSION_USER_KEY] = user
        st.session_state[SESSION_ROLE_KEY] = user["role"]
    return user


def require_user() -> Optional[Dict[str, Any]]:
    """Return the current user or stop the page with a clear demo message."""

    user = get_current_user()
    if not user:
        st.warning("Please select a demo user to continue.")
        st.stop()
    return user


def has_permission(permission_name: str) -> bool:
    """Return whether the current demo user has a permission."""

    user = get_current_user()
    if not user:
        return False
    return role_has_permission(user["role"], permission_name)


def require_permission(permission_name: str) -> bool:
    """Show an access-denied message and stop if permission is absent."""

    if has_permission(permission_name):
        return True
    st.warning("You do not have access to this page in the current demo role.")
    st.caption("Switch demo user in the sidebar to view another role's prototype access.")
    st.stop()
    return False


def render_user_selector(location: str = "sidebar") -> Optional[Dict[str, Any]]:
    """Render a fake demo user selector in the sidebar or page body."""

    initialise_mock_session()
    users = list_demo_users()
    if not users:
        st.warning("No demo users are available. Database initialisation may have failed.")
        return None

    current_user = get_current_user() or users[0]
    current_index = 0
    for index, user in enumerate(users):
        if int(user["id"]) == int(current_user["id"]):
            current_index = index
            break

    def format_user(user_id: int) -> str:
        user = _find_user(user_id)
        if not user:
            return "Unknown demo user"
        return "%s — %s" % (user["display_name"], user["role"])

    container = st.sidebar if location == "sidebar" else st
    selected_id = container.selectbox(
        "Demo user",
        options=[int(user["id"]) for user in users],
        index=current_index,
        format_func=format_user,
        help="Prototype-only demo user selector. This is not authentication.",
    )
    selected_user = set_current_user(int(selected_id))
    if selected_user:
        container.caption("Prototype only — no real authentication or passwords are implemented.")
    return selected_user


def render_role_selector() -> str:
    """Legacy wrapper that now renders the Step 3 demo user selector."""

    user = render_user_selector()
    if user:
        return user["role"]
    return HCP.key


def current_role_key() -> str:
    """Return the current demo user's role key."""

    user = get_current_user()
    if user:
        return user["role"]
    return HCP.key


def current_role_label() -> str:
    """Return the current demo user's role display label."""

    return get_role_label(current_role_key())


def has_role(role_key: str) -> bool:
    """Return whether the current demo user has a role."""

    return current_role_key() == role_key and role_key in ROLE_BY_KEY
