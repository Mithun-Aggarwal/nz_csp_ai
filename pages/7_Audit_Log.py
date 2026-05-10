"""Audit log page for Step 3 persisted audit events."""

import streamlit as st

from config.roles import PERMISSION_VIEW_AUDIT_LOG
from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.audit_service import list_audit_events
from services.auth_service import render_user_selector, require_permission, require_user

initialise_database()
st.set_page_config(page_title="Audit Log | %s" % APP_NAME, page_icon="📋", layout="wide")
st.sidebar.title(APP_NAME)
render_user_selector()
st.sidebar.info(APP_STATUS)

user = require_user()
require_permission(PERMISSION_VIEW_AUDIT_LOG)

st.title("Audit Log")
st.write("Current demo user: **%s** (%s)" % (user["display_name"], user["role"]))
st.info("Step 3 persists simple audit events for demo programme record creation.")

records = list_audit_events()
if records:
    st.dataframe([record.__dict__ for record in records], use_container_width=True, hide_index=True)
else:
    st.warning("No audit log records have been created yet. Creating a demo programme record will add an audit event.")
