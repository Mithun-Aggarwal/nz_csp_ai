"""Audit log placeholder page."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.audit_service import list_audit_events
from services.auth_service import current_role_label, render_role_selector

st.set_page_config(page_title=f"Audit Log | {APP_NAME}", page_icon="📋", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("Audit Log")
st.write(f"Current mock role: **{current_role_label()}**")
st.info(
    "Future scope: immutable-style user action history, approvals, verification, "
    "and override traceability."
)

records = list_audit_events()
if records:
    st.dataframe(
        [
            {
                "actor": record.actor,
                "action": record.action,
                "entity_type": record.entity_type,
                "entity_id": record.entity_id,
                "created_at": record.created_at.isoformat(),
            }
            for record in records
        ],
        use_container_width=True,
    )
else:
    st.warning(
        "No audit log records have been created yet. Audit persistence will be "
        "added in a future prototype step."
    )
