"""Notification log page for Step 3 simulated notifications."""

import streamlit as st

from config.roles import PERMISSION_VIEW_NOTIFICATIONS
from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.auth_service import render_user_selector, require_permission, require_user
from services.notification_service import list_notifications

initialise_database()
st.set_page_config(page_title="Notification Log | %s" % APP_NAME, page_icon="✉️", layout="wide")
st.sidebar.title(APP_NAME)
render_user_selector()
st.sidebar.info(APP_STATUS)

user = require_user()
require_permission(PERMISSION_VIEW_NOTIFICATIONS)

st.title("Notification Log")
st.write("Current demo user: **%s** (%s)" % (user["display_name"], user["role"]))
st.info("Notifications are simulated only. No real email is sent in this prototype.")

records = list_notifications()
if records:
    st.dataframe([record.__dict__ for record in records], use_container_width=True, hide_index=True)
else:
    st.warning("No notification records have been created yet. Creating a demo programme record will add a simulated notification.")
