"""Streamlit entry point for the Blenrep NZ CSP Portal prototype."""

import streamlit as st

from config.roles import get_role_permissions
from config.settings import APP_NAME, APP_STATUS
from database.db import DatabaseInitialisationError, initialise_database
from services.auth_service import get_current_user, render_user_selector


def main() -> None:
    """Render the prototype home page."""

    st.set_page_config(page_title=APP_NAME, page_icon="💊", layout="wide")
    try:
        initialise_database()
    except DatabaseInitialisationError as exc:
        st.error("Database initialisation failed: %s" % exc)
        st.stop()

    st.sidebar.title(APP_NAME)
    render_user_selector()
    st.sidebar.info(APP_STATUS)

    user = get_current_user()

    st.title(APP_NAME)
    st.caption(APP_STATUS)
    st.info(
        "Step 3 makes this proof-of-concept behave like a basic mock role-based "
        "portal with fake demo users, SQLite-backed demo programme records, "
        "simulated audit events, and simulated notification events."
    )

    st.warning("Prototype only — do not enter real patient-identifying information.")

    st.subheader("Current demo user")
    if user:
        st.write("**Name:** %s" % user["display_name"])
        st.write("**Role:** %s" % user["role"])
        st.write("**Organisation:** %s" % user.get("organisation", ""))
        st.write("**Email:** %s" % user["email"])
        st.caption("This is mock authentication only. No password or real credential is used.")

        st.subheader("Current permissions")
        st.write(", ".join(get_role_permissions(user["role"])) or "No permissions configured.")

    st.subheader("Prototype navigation")
    st.write(
        "Use the Streamlit pages in the sidebar to open role-aware prototype pages. "
        "Pages remain visible in navigation, but each page checks the selected demo "
        "user's permissions and shows access denied where appropriate."
    )


if __name__ == "__main__":
    main()
