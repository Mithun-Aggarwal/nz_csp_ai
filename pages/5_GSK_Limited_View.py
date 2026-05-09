"""GSK limited-view placeholder page."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.auth_service import current_role_label, render_role_selector

st.set_page_config(page_title=f"GSK Limited View | {APP_NAME}", page_icon="👁️", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("GSK Limited View")
st.write(f"Current mock role: **{current_role_label()}**")
st.warning("This future view must remain dashboard-only and non-sensitive. No critical patient information should be exposed.")
st.info("Future scope: high-level milestone visibility for scarcity / stock approval coordination only.")
