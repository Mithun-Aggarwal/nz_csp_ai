"""Notification log placeholder page."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.auth_service import current_role_label, render_role_selector
from services.notification_service import build_milestone_notification

st.set_page_config(page_title=f"Notification Log | {APP_NAME}", page_icon="✉️", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("Notification Log")
st.write(f"Current mock role: **{current_role_label()}**")
st.info("Future scope: simulated and real notification history with approved non-sensitive content rules.")
example = build_milestone_notification("gsk_limited_viewer", "free dose period active")
st.json({**example.__dict__, "created_at": example.created_at.isoformat()}, expanded=False)
