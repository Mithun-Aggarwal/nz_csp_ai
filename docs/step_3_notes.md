# Step 3 Notes — Mock Role-Based Portal

## Purpose

Step 3 makes the Blenrep NZ CSP Portal proof-of-concept behave like a basic role-based portal without implementing production authentication or the full business workflow. The goal is to demonstrate fake user selection, session state, central permissions, first record creation, and simulated audit/notification events.

## Mock user model

The app seeds four fake users into SQLite on startup. The selected user is stored in Streamlit session state as `st.session_state["current_user"]`.

| User | Role | Email | Organisation |
| --- | --- | --- | --- |
| Dr Amelia Smith | HCP | amelia.smith@example.test | Auckland Private Haematology |
| Priya Patel | Pharmacist | priya.patel@example.test | Auckland Oncology Pharmacy |
| Alex Morgan | CSP Admin | alex.morgan@example.test | CSP Vendor Admin |
| GSK Programme Viewer | GSK Limited Viewer | gsk.viewer@example.test | GSK NZ |

This is mock authentication only. There is no password handling, MFA, SSO, identity-provider integration, or credential storage.

## Role/permission matrix

| Permission | HCP | Pharmacist | CSP Admin | GSK Limited Viewer |
| --- | --- | --- | --- | --- |
| `can_create_programme_record` | Yes | Yes | Yes | No |
| `can_view_own_programme_records` | Yes | Yes | No | No |
| `can_view_all_programme_records` | No | No | Yes | No |
| `can_view_limited_dashboard` | No | No | No | Yes |
| `can_view_notifications` | No | No | Yes | No |
| `can_view_audit_log` | No | No | Yes | No |
| `can_access_csp_admin` | No | No | Yes | No |
| `can_prepare_programme_record` | No | Yes | Yes | No |
| `can_submit_programme_record` | Yes | No | Yes | No |

CSP Admin can also access the GSK Limited View for prototype convenience, but the page still shows only aggregate non-sensitive data.

## Basic programme record creation flow

1. A permitted HCP or Pharmacist selects their fake demo user.
2. They open the HCP Portal or Pharmacist Portal.
3. They enter only fake/demo operational fields:
   - clinic patient code / demo programme ID,
   - site / clinic name,
   - treating HCP name,
   - first paid-dose date.
4. The app writes a row to the `patients` table, treating it as a demo programme-record table for now.
5. Default statuses are deliberately simple:
   - HCP-created records use `draft_created_by_hcp`.
   - Pharmacist-created records use `draft_prepared_by_pharmacist`.

No patient name, DOB, NHI number, address, clinical details, evidence upload, free-dose calculation, or reorder workflow is collected or implemented.

## Audit and notification behaviour

When a programme record is created:

- `services.audit_service.create_audit_event()` inserts an `audit_log` row with `event_action = programme_record_created`.
- `services.notification_service.create_programme_record_notification()` inserts a `notifications` row for the CSP Admin role with status `simulated`.
- No email is sent.
- CSP Admin can view the Audit Log and Notification Log pages.

## Role-based page access

Pages remain visible in Streamlit navigation, but each page checks the current demo user's permissions. If the selected role does not have access, the page displays:

> You do not have access to this page in the current demo role.

## Deferred to later steps

The following remain intentionally out of scope:

- real authentication, passwords, MFA, SSO, and production security,
- full patient lifecycle and workflow state transitions,
- paid-dose verification and free-dose eligibility calculation,
- reorder workflow and vial calculator logic,
- evidence uploads,
- real email sending,
- GSK record-level access,
- production privacy, hosting, retention, and compliance controls.
