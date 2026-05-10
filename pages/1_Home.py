"""Home page for the Step 3 mock role-based portal."""

import streamlit as st

from config.roles import get_role_permissions
from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.auth_service import get_current_user, render_user_selector

initialise_database()
st.set_page_config(page_title="Home | %s" % APP_NAME, page_icon="🏠", layout="wide")
st.sidebar.title(APP_NAME)
render_user_selector()
st.sidebar.info(APP_STATUS)

user = get_current_user()

st.title("Home")
st.write("Welcome to the Blenrep NZ CSP Portal proof-of-concept.")
st.warning("Prototype only — do not enter real patient-identifying information.")

st.subheader("Current demo user")
if user:
    st.write("**Name:** %s" % user["display_name"])
    st.write("**Role:** %s" % user["role"])
    st.write("**Organisation:** %s" % user.get("organisation", ""))
    st.caption("This is mock authentication only. No real login, password, MFA, or email sending is implemented.")
    st.write("**Permissions:** %s" % (", ".join(get_role_permissions(user["role"])) or "None"))

st.info("Workflow logic will be expanded in later steps. Step 3 focuses on mock roles, record creation, audit logging, and simulated notifications.")
