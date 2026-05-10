"""HCP portal page with Step 3 demo programme record creation."""

import sqlite3
from datetime import date

import streamlit as st

from config.roles import PERMISSION_CREATE_PROGRAMME_RECORD, PERMISSION_VIEW_ALL_PROGRAMME_RECORDS, PERMISSION_VIEW_OWN_PROGRAMME_RECORDS
from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.auth_service import get_current_user, has_permission, render_user_selector, require_permission, require_user
from services.workflow_service import create_programme_record, list_all_programme_records, list_programme_records_for_user

initialise_database()
st.set_page_config(page_title="HCP Portal | %s" % APP_NAME, page_icon="🩺", layout="wide")
st.sidebar.title(APP_NAME)
render_user_selector()
st.sidebar.info(APP_STATUS)

user = require_user()
if not (has_permission(PERMISSION_VIEW_OWN_PROGRAMME_RECORDS) or has_permission(PERMISSION_VIEW_ALL_PROGRAMME_RECORDS)):
    require_permission(PERMISSION_VIEW_OWN_PROGRAMME_RECORDS)

st.title("HCP Portal")
st.write("Current demo user: **%s** (%s)" % (user["display_name"], user["role"]))
st.warning("Prototype only — do not enter real patient-identifying information.")
st.info("Create a basic demo programme record using only fake operational identifiers. Workflow logic will be expanded in later steps.")

if has_permission(PERMISSION_CREATE_PROGRAMME_RECORD):
    with st.form("hcp_create_programme_record"):
        st.subheader("Create demo programme record")
        clinic_patient_code = st.text_input("Clinic patient code / demo programme ID")
        site_name = st.text_input("Site / clinic name", value=user.get("organisation", ""))
        treating_hcp_name = st.text_input("Treating HCP name", value=user["display_name"])
        first_paid_dose_date = st.date_input("First paid dose date", value=date.today())
        submitted = st.form_submit_button("Create demo record")

    if submitted:
        if not clinic_patient_code.strip() or not site_name.strip() or not treating_hcp_name.strip():
            st.error("Please enter a fake programme ID, site/clinic name, and treating HCP name.")
        else:
            try:
                record_id = create_programme_record(
                    clinic_patient_code=clinic_patient_code,
                    site_name=site_name,
                    treating_hcp_name=treating_hcp_name,
                    first_paid_dose_date=first_paid_dose_date,
                    current_user=user,
                )
                st.success("Demo programme record %s created. Audit and notification events were simulated." % record_id)
            except sqlite3.IntegrityError:
                st.error("That clinic patient code / demo programme ID already exists. Use a different fake value.")
else:
    st.caption("This demo role cannot create programme records.")

records = list_all_programme_records() if has_permission(PERMISSION_VIEW_ALL_PROGRAMME_RECORDS) else list_programme_records_for_user(user)
st.subheader("Programme records")
if has_permission(PERMISSION_VIEW_ALL_PROGRAMME_RECORDS):
    st.caption("CSP Admin view: showing all demo records from the HCP Portal.")
else:
    st.caption("Showing demo records created by the selected HCP user.")

if records:
    st.dataframe(records, use_container_width=True, hide_index=True)
else:
    st.info("No demo programme records have been created for this view yet.")
