"""Home page placeholder."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.auth_service import current_role_label, render_role_selector

st.set_page_config(page_title=f"Home | {APP_NAME}", page_icon="🏠", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("Home")
st.write("Welcome to the Blenrep NZ CSP Portal proof-of-concept.")
st.write(f"Current mock role: **{current_role_label()}**")
st.info("This page will become the landing dashboard and orientation page.")
