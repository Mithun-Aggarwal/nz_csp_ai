"""Audit log placeholder page."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.audit_service import create_audit_event
from services.auth_service import current_role_label, render_role_selector

st.set_page_config(page_title=f"Audit Log | {APP_NAME}", page_icon="📋", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("Audit Log")
st.write(f"Current mock role: **{current_role_label()}**")
st.info("Future scope: immutable-style user action history, approvals, verification, and override traceability.")
example = create_audit_event(actor=current_role_label(), action="view_placeholder", entity_type="page", entity_id="audit_log")
st.json({**example.__dict__, "created_at": example.created_at.isoformat()}, expanded=False)
