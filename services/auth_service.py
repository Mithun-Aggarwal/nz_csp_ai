"""Mock authentication and role-selection helpers.

This module deliberately does not implement production authentication or store
passwords. It only supports a prototype role context for Streamlit pages.
"""

import streamlit as st

from config.roles import HCP, ROLE_BY_KEY, get_role_label, role_options

SESSION_ROLE_KEY = "mock_role_key"


def initialise_mock_session() -> None:
    """Ensure a default mock role exists in the Streamlit session."""

    if SESSION_ROLE_KEY not in st.session_state:
        st.session_state[SESSION_ROLE_KEY] = HCP.key


def render_role_selector() -> str:
    """Render a sidebar mock role selector and return the selected role key."""

    initialise_mock_session()
    selected = st.sidebar.selectbox(
        "Mock role",
        options=role_options(),
        index=role_options().index(st.session_state[SESSION_ROLE_KEY]),
        format_func=get_role_label,
        help="Prototype-only role selector. This is not authentication.",
    )
    st.session_state[SESSION_ROLE_KEY] = selected
    st.sidebar.caption("Prototype only — no real authentication is implemented.")
    return selected


def current_role_key() -> str:
    """Return the current mock role key."""

    initialise_mock_session()
    return st.session_state[SESSION_ROLE_KEY]


def current_role_label() -> str:
    """Return the current mock role display label."""

    return get_role_label(current_role_key())


def has_role(role_key: str) -> bool:
    """Placeholder for future role checks."""

    return current_role_key() == role_key and role_key in ROLE_BY_KEY
