"""Restricted aggregate-only GSK limited-view page."""

import streamlit as st

from config.roles import PERMISSION_ACCESS_CSP_ADMIN, PERMISSION_VIEW_LIMITED_DASHBOARD
from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.auth_service import has_permission, render_user_selector, require_permission, require_user
from services.notification_service import count_notifications
from services.workflow_service import get_programme_record_counts

initialise_database()
st.set_page_config(page_title="GSK Limited View | %s" % APP_NAME, page_icon="👁️", layout="wide")
st.sidebar.title(APP_NAME)
render_user_selector()
st.sidebar.info(APP_STATUS)

user = require_user()
if not (has_permission(PERMISSION_VIEW_LIMITED_DASHBOARD) or has_permission(PERMISSION_ACCESS_CSP_ADMIN)):
    require_permission(PERMISSION_VIEW_LIMITED_DASHBOARD)

st.title("GSK Limited View")
st.write("Current demo user: **%s** (%s)" % (user["display_name"], user["role"]))
st.warning("Restricted aggregate-only prototype view. No clinic patient codes or record-level details are shown.")
st.info("This view is limited to high-level non-sensitive counts. Workflow logic will be expanded in later steps.")

counts = get_programme_record_counts()
notification_count = count_notifications()

cols = st.columns(3)
cols[0].metric("Total demo programme records", counts["total"])
cols[1].metric("Statuses represented", len(counts["by_status"]))
cols[2].metric("Simulated notifications", notification_count)

st.subheader("Aggregate records by status")
if counts["by_status"]:
    st.dataframe(counts["by_status"], use_container_width=True, hide_index=True)
else:
    st.info("No aggregate programme data is available yet.")
