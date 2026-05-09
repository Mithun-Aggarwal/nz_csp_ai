"""CSP Admin placeholder page."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.auth_service import current_role_label, render_role_selector

st.set_page_config(page_title=f"CSP Admin | {APP_NAME}", page_icon="🛠️", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("CSP Admin")
st.write(f"Current mock role: **{current_role_label()}**")
st.info("Future scope: user approvals, patient verification, record reopen/override, work queues, and governance reporting.")
st.columns(4)[0].metric("User approvals", "0")
st.columns(4)[1].metric("Pending verification", "0")
st.columns(4)[2].metric("Expiring periods", "0")
st.columns(4)[3].metric("Overrides", "0")
