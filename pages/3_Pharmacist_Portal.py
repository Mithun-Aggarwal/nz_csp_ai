"""Pharmacist portal placeholder page."""

import streamlit as st

from config.settings import APP_NAME, APP_STATUS
from services.auth_service import current_role_label, render_role_selector

st.set_page_config(page_title=f"Pharmacist Portal | {APP_NAME}", page_icon="💊", layout="wide")
st.sidebar.title(APP_NAME)
render_role_selector()
st.sidebar.info(APP_STATUS)

st.title("Pharmacist Portal")
st.write(f"Current mock role: **{current_role_label()}**")
st.info("Future scope: prepare patient records, support paid-dose attestations, manage reorder tasks, and record manual transactions.")
st.columns(3)[0].metric("Records in preparation", "0")
st.columns(3)[1].metric("Reorders due", "0")
st.columns(3)[2].metric("Transactions recorded", "0")
