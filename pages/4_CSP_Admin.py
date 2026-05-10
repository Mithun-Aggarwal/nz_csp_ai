"""CSP Admin page for Step 3 record and aggregate dashboard."""

import streamlit as st

from config.roles import PERMISSION_ACCESS_CSP_ADMIN
from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.auth_service import render_user_selector, require_permission, require_user
from services.workflow_service import get_programme_record_counts, list_all_programme_records

initialise_database()
st.set_page_config(page_title="CSP Admin | %s" % APP_NAME, page_icon="🛠️", layout="wide")
st.sidebar.title(APP_NAME)
render_user_selector()
st.sidebar.info(APP_STATUS)

user = require_user()
require_permission(PERMISSION_ACCESS_CSP_ADMIN)

st.title("CSP Admin")
st.write("Current demo user: **%s** (%s)" % (user["display_name"], user["role"]))
st.info("Step 3 admin view shows demo records and counts only. Deeper verification workflow comes later.")

counts = get_programme_record_counts()
records = list_all_programme_records()

cols = st.columns(3)
cols[0].metric("Total demo programme records", counts["total"])
cols[1].metric("Statuses represented", len(counts["by_status"]))
cols[2].metric("Admin workflow depth", "Later")

st.subheader("Records by status")
if counts["by_status"]:
    st.dataframe(counts["by_status"], use_container_width=True, hide_index=True)
else:
    st.info("No records have been created yet.")

st.subheader("All demo programme records")
if records:
    st.dataframe(records, use_container_width=True, hide_index=True)
else:
    st.info("No demo programme records have been created yet.")
