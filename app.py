"""Streamlit entry point for the Blenrep NZ CSP Portal prototype."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.auth_service import current_role_label, render_role_selector


def main() -> None:
    """Render the prototype home page."""

    st.set_page_config(page_title=APP_NAME, page_icon="💊", layout="wide")
    initialise_database()

    st.sidebar.title(APP_NAME)
    render_role_selector()
    st.sidebar.info(APP_STATUS)

    st.title(APP_NAME)
    st.caption(APP_STATUS)
    st.info(
        "This prototype currently provides only the Step 1 technical foundation: "
        "role placeholders, page skeletons, draft database schema, and service boundaries."
    )

    st.subheader("Current mock role")
    st.write(f"You are viewing the portal as: **{current_role_label()}**")

    st.subheader("Prototype navigation")
    st.write(
        "Use the Streamlit pages in the sidebar to view placeholder portals for HCPs, "
        "pharmacists, CSP Admin, GSK limited visibility, notifications, and audit logs."
    )

    st.warning(
        "No real patient data, production authentication, clinical decision support, or real "
        "email sending is implemented in this Step 1 skeleton."
    )


if __name__ == "__main__":
    main()
