"""Pharmacist portal page with Step 3 demo programme record preparation."""

import sqlite3
from datetime import date

import streamlit as st

from config.roles import PERMISSION_CREATE_PROGRAMME_RECORD, PERMISSION_PREPARE_PROGRAMME_RECORD, PERMISSION_VIEW_ALL_PROGRAMME_RECORDS, PERMISSION_VIEW_OWN_PROGRAMME_RECORDS
from config.settings import APP_NAME, APP_STATUS
from database.db import initialise_database
from services.auth_service import has_permission, render_user_selector, require_permission, require_user
from services.workflow_service import create_programme_record, list_all_programme_records, list_programme_records_for_user

initialise_database()
st.set_page_config(page_title="Pharmacist Portal | %s" % APP_NAME, page_icon="💊", layout="wide")
st.sidebar.title(APP_NAME)
render_user_selector()
st.sidebar.info(APP_STATUS)

user = require_user()
if not (has_permission(PERMISSION_PREPARE_PROGRAMME_RECORD) or has_permission(PERMISSION_VIEW_ALL_PROGRAMME_RECORDS)):
    require_permission(PERMISSION_PREPARE_PROGRAMME_RECORD)

st.title("Pharmacist Portal")
st.write("Current demo user: **%s** (%s)" % (user["display_name"], user["role"]))
st.warning("Prototype only — do not enter real patient-identifying information.")
st.info("Pharmacists can prepare a basic demo programme record. Reorder and paid-dose workflows are deferred.")

if has_permission(PERMISSION_CREATE_PROGRAMME_RECORD) and has_permission(PERMISSION_PREPARE_PROGRAMME_RECORD):
    with st.form("pharmacist_create_programme_record"):
        st.subheader("Prepare demo programme record")
        clinic_patient_code = st.text_input("Clinic patient code / demo programme ID")
        site_name = st.text_input("Site / clinic name", value=user.get("organisation", ""))
        treating_hcp_name = st.text_input("Treating HCP name")
        first_paid_dose_date = st.date_input("First paid dose date", value=date.today())
        submitted = st.form_submit_button("Prepare demo record")

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
                st.success("Demo programme record %s prepared. Audit and notification events were simulated." % record_id)
            except sqlite3.IntegrityError:
                st.error("That clinic patient code / demo programme ID already exists. Use a different fake value.")

records = list_all_programme_records() if has_permission(PERMISSION_VIEW_ALL_PROGRAMME_RECORDS) else list_programme_records_for_user(user)
st.subheader("Prepared programme records")
if has_permission(PERMISSION_VIEW_ALL_PROGRAMME_RECORDS):
    st.caption("CSP Admin view: showing all demo records from the Pharmacist Portal.")
else:
    st.caption("Showing demo records prepared by the selected pharmacist user.")

if records:
    st.dataframe(records, use_container_width=True, hide_index=True)
else:
    st.info("No demo programme records have been created for this view yet.")
