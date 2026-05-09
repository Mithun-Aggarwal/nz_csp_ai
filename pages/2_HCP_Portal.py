"""HCP portal placeholder page."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.auth_service import current_role_label, render_role_selector

st.set_page_config(page_title=f"HCP Portal | {APP_NAME}", page_icon="🩺", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("HCP Portal")
st.write(f"Current mock role: **{current_role_label()}**")
st.info("Future scope: allocated patient dashboard, registration review, final submission, and milestone confirmation.")
st.columns(3)[0].metric("Draft records", "0")
st.columns(3)[1].metric("Awaiting approval", "0")
st.columns(3)[2].metric("Active free-dose patients", "0")
