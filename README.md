# Blenrep NZ CSP Portal Prototype

This repository contains a Python/Streamlit proof-of-concept for the **Blenrep NZ CSP Portal**. The portal concept is based on the uploaded BRD and is intended to explore a reusable administrative architecture for role-based workflow, patient programme records, audit trail, notifications, and database-backed state.

> **Current status:** Step 1 architecture skeleton only. This is not a production healthcare system and must not be used with real patient information.

## Purpose

The prototype supports early technical discovery for a New Zealand cost-share / paid-to-free programme administration portal. The intended future portal will help coordinate administrative workflow between private haematologists, pharmacists, CSP Admin, and a restricted GSK Programme Admin view where approved.

The portal is intentionally positioned as **administrative and non-clinical**. It does not provide prescribing decisions, treatment advice, clinical decision support, HCL workflow management, inventory management, or reconstitution-provider workflow.

## What Is Included in Step 1

- Streamlit application entry point: `app.py`.
- Page skeletons for Home, HCP, Pharmacist, CSP Admin, GSK Limited View, Notification Log, and Audit Log.
- Mock role selector for prototype navigation only.
- Placeholder service modules for authentication, workflow, notifications, and audit.
- Placeholder model modules for users, patients, orders, and paid-dose records.
- Draft SQLite schema for discussion.
- Technical understanding document at `docs/technical_understanding.md`.

## What Is Not Included Yet

- Full business workflow implementation.
- Production authentication, passwords, MFA, SSO, or identity-provider integration.
- Real patient data or real clinical information.
- Real email sending.
- Direct integration to HCL, wholesalers, inventory systems, or reconstitution providers.
- Final vial calculator logic.
- Production hosting, privacy, security, validation, or compliance controls.

## Project Structure

```text
app.py
pages/
  1_Home.py
  2_HCP_Portal.py
  3_Pharmacist_Portal.py
  4_CSP_Admin.py
  5_GSK_Limited_View.py
  6_Notification_Log.py
  7_Audit_Log.py

database/
  db.py
  schema.sql

services/
  auth_service.py
  workflow_service.py
  notification_service.py
  audit_service.py

models/
  users.py
  patients.py
  orders.py

config/
  roles.py
  settings.py

docs/
  technical_understanding.md

README.md
requirements.txt
```


## Local Setup on Mac

```bash
git clone https://github.com/Mithun-Aggarwal/nz_csp_ai.git
cd nz_csp_ai

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

streamlit run app.py
```

## Install Dependencies

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

The app will initialise a local SQLite database at `database/app.db` if needed. This file is for local prototype use only and should not contain real patient data.

## Development Notes

- Keep UI, services, models, database access, and configuration separate.
- Do not put real patient data in the repository or local demo database.
- Do not implement real email sending until approved templates, recipients, and privacy rules are confirmed.
- Do not implement production authentication until the identity, security, and MFA model is confirmed.
- Treat the GSK limited view as non-sensitive, dashboard-only visibility unless business approval changes that scope.

## Next Suggested Development Steps

1. Confirm final workflow states and allowed transitions.
2. Confirm the reorder submission and approval model.
3. Confirm minimum patient/programme data fields and privacy requirements.
4. Confirm paid-dose evidence requirements and retention rules.
5. Define notification triggers, recipients, templates, and escalation rules.
6. Add mock data factories and read-only dashboards for the next prototype step.
7. Implement role-aware page guards and database-backed records.
8. Add a validated vial calculator module once business rules are provided.
9. Prepare security, privacy, hosting, and audit-control design for production planning.

## Step 3 — Mock Role-Based Portal

Step 3 turns the skeleton into a basic mock role-based portal with fake demo users, Streamlit session state, SQLite-backed demo programme records, and simulated audit/notification logging.

### Run the app locally

```bash
streamlit run app.py
```

On startup, the app initialises `database/app.db`, applies lightweight local schema migrations, and idempotently seeds four fake demo users.

### Select a demo user

Use the **Demo user** selector in the sidebar or on the home page. The selected fake user is stored in Streamlit session state as `st.session_state["current_user"]`.

Available fake users:

| Demo user | Role | Prototype access |
| --- | --- | --- |
| Dr Amelia Smith | HCP | Create demo programme records, view own records, submit permission placeholder. |
| Priya Patel | Pharmacist | Prepare/create demo programme records and view own records. |
| Alex Morgan | CSP Admin | View all records, CSP Admin page, Audit Log, Notification Log, and admin dashboards. |
| GSK Programme Viewer | GSK Limited Viewer | View aggregate-only, non-sensitive dashboard counts. |

### Important prototype boundaries

- This is **mock authentication only**; there are no passwords, MFA, SSO, or real credentials.
- Do **not** enter real patient-identifying information.
- Programme records collect only fake/demo operational identifiers such as clinic patient code, site, treating HCP name, and first paid-dose date.
- Audit and notification logs are simulated SQLite records.
- No real email is sent.
- Paid-dose verification, free-dose eligibility, reorder workflow, vial calculator logic, evidence uploads, and production security are intentionally deferred.
