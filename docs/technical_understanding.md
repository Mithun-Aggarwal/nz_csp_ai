# Blenrep NZ CSP Portal — Step 1 Technical Understanding

## Source Reviewed

- `Docs/Blenrep_NZ_CSP_Portal_BRD_V1_2.docx`
- `Docs/Blenrep_NZ_CSP_Portal_BRD_V1_2.pdf`

This document translates the BRD into a concise technical baseline for a Streamlit proof-of-concept. It is not a final functional specification and should be validated with business, privacy, security, and clinical governance stakeholders before production design.

## Business Process Summary

The Blenrep NZ CSP Portal is intended to support administration of a New Zealand cost-share / paid-to-free programme. The patient begins treatment outside the portal on a private paid pathway. The first three doses/cycles are privately funded. Before cycle 4, the patient should be registered in the portal using a clinic patient ID/code. Once the first three paid doses are confirmed and CSP Admin verifies eligibility information, the patient becomes eligible for free doses.

The free-dose period is calculated from the first paid dose date and runs for one year. During active treatment, reorder-related activity and manual transaction/order records are captured against the patient record. At the end of the one-year period, the patient returns to a new paid pathway status while the same longitudinal patient record remains active for history and future cycles.

The portal is administrative and non-clinical. It does not make prescribing, treatment, eye-care, wholesaler, reconstitution, HCL, or stock-release decisions. It may generate high-level, non-sensitive milestone notifications to GSK Programme Admin and CSP Admin for scarcity / stock approval coordination, but formal HCL-side processes remain outside portal scope.

## Core Users and Roles

| Role | Primary intent | Expected access pattern |
| --- | --- | --- |
| Private Haematologist / HCP | Final submitter for initial patient registration; may create records directly, review pharmacist-prepared records, confirm milestones, and view allocated patients. | Role-based access to allocated patient records only. |
| Private Pharmacist | Supports operational data entry, saves records for HCP approval, supports paid-dose confirmation, records manual transactions, and manages reorder-related activity. | Role-based access to allocated patients and/or relevant site relationships. |
| CSP Admin | Full portal administrator and administrative owner for user approvals, role correction, record verification, reopening, overrides, and broad operational visibility. | Broad operational access across programme records. |
| GSK Limited Viewer / GSK Programme Admin | Optional restricted, dashboard-only operational stakeholder for non-sensitive milestones related to scarcity / stock approval handling. | Highly restricted view; no critical or sensitive patient information. |

### Out-of-Scope Actors

- Patients.
- Eye-care professionals.
- HCL users.
- Reconstitution providers.

## In Scope for the Portal

- Standalone NZ web portal prototype foundation.
- Role-aware Streamlit page structure.
- User self-registration and CSP Admin approval concept.
- Patient registration prior to cycle 4.
- Clinic patient ID/code as the preferred operational identifier.
- Pharmacist-prepared records with haematologist final submission assumption.
- CSP Admin verification and administrative oversight.
- First-three-paid-dose attestation/confirmation concept.
- Free-dose period calculation from first paid dose date.
- Patient lifecycle state tracking.
- Reorder workflow placeholders.
- Manual transaction/order recording placeholders.
- Dashboard, notification, and audit placeholders.
- Vial calculator placeholder; detailed logic is deferred.

## Out of Scope for This Prototype Step

- Full business workflow implementation.
- Production authentication, passwords, MFA, or identity provider integration.
- Real patient data or real clinical data capture.
- Real email sending.
- Direct HCL, wholesaler, inventory, or reconstitution-provider integration.
- Formal stock approval status tracking.
- Clinical decision support, prescribing decisions, or dose calculator logic.
- Final data model, final security model, or production hosting architecture.

## Proposed Application Modules

| Module | Purpose |
| --- | --- |
| `app.py` | Streamlit landing page and session bootstrap. |
| `pages/` | Role/workflow-oriented Streamlit pages. |
| `config/roles.py` | Central role names and role metadata. |
| `config/settings.py` | Prototype-level settings and paths. |
| `database/db.py` | SQLite connection and schema initialisation helpers. |
| `database/schema.sql` | Draft database structure for future workflow data. |
| `services/auth_service.py` | Mock role selection and future authentication boundary. |
| `services/workflow_service.py` | Workflow state constants and future transition logic. |
| `services/notification_service.py` | Simulated notification creation and future email boundary. |
| `services/audit_service.py` | Audit trail helper placeholders. |
| `models/users.py` | User dataclasses/placeholders. |
| `models/patients.py` | Patient dataclasses/placeholders. |
| `models/orders.py` | Order and paid-dose record dataclasses/placeholders. |
| `docs/technical_understanding.md` | BRD analysis and technical foundation notes. |

## Proposed Pages

| Page | Intended future functionality |
| --- | --- |
| Home | Portal overview, current prototype status, mock role selector. |
| HCP Portal | HCP dashboard, allocated patient list, registration approval/submission queue. |
| Pharmacist Portal | Pharmacist data-entry queue, reorder work queue, paid-dose confirmation support. |
| CSP Admin | User approvals, patient verification, reopen/override tools, programme work queues. |
| GSK Limited View | Restricted, non-sensitive milestone dashboard only. |
| Notification Log | Simulated notification history and future delivery status view. |
| Audit Log | Placeholder for user action history and governance traceability. |

## Proposed Database Tables

| Table | Draft purpose |
| --- | --- |
| `users` | Portal users, mock role, approval status, site/organisation reference. |
| `patients` | Longitudinal patient programme record using clinic patient ID/code. |
| `orders` | Manual order/reorder transaction records associated with a patient. |
| `paid_dose_records` | Attestation and verification records for paid doses/cycles. |
| `notifications` | Simulated in-app/email notification records. |
| `audit_log` | Immutable-style action log for governance and traceability. |

## Key Workflow States

Initial proposed states for discussion:

1. `draft_prepared_by_pharmacist`
2. `draft_created_by_hcp`
3. `submitted_for_hcp_approval`
4. `submitted_for_csp_verification`
5. `paid_doses_pending_confirmation`
6. `paid_doses_confirmed`
7. `eligible_for_free_doses`
8. `active_free_dose_period`
9. `free_dose_period_expiring`
10. `reset_to_paid_pathway`
11. `closed_or_discontinued`

These are deliberately draft states. The BRD explicitly notes that exact statuses and transitions require later confirmation.

## Business Rules to Convert Into Application Logic Later

- Patient starts on a private paid pathway outside the portal.
- Patient should be registered before cycle 4.
- First 3 doses/cycles must be privately funded.
- Pharmacist may prepare records; haematologist is assumed to be final submitter for initial registration.
- Clinic patient ID/code is the preferred operational identifier.
- Paid-dose confirmation may come from pharmacist and/or haematologist.
- CSP Admin verifies eligibility-related confirmation.
- Free-dose eligibility begins after paid-dose requirements are confirmed and verified.
- Free-dose period concludes one year from the first paid dose date.
- After expiry, the patient returns to a paid pathway status.
- The same patient record remains active across repeated periods.
- Reorders are in scope, but the final approval/submission model is open.
- Portal milestone notifications should contain non-sensitive operational information only.
- GSK Programme Admin visibility must be highly restricted and non-sensitive.
- The portal must remain non-clinical and administrative.

## Sensitive Data Considerations

- Patient-related information is sensitive and must be handled with strict access control and auditability.
- The prototype must not include real patient data.
- Clinic patient ID/code should be treated as sensitive operational programme information even if it is less identifying than full demographics.
- GSK Limited Viewer should not see critical or sensitive patient information.
- Email notifications should avoid sensitive details and direct users to log in for role-appropriate information.
- Evidence uploads, if later approved, will require a separate privacy, retention, storage, and access-control design.
- Production implementation will require secure authentication, MFA considerations, encrypted transport/storage design, retention policy, hosting controls, and alignment with NZ requirements and GSK policies.

## Assumptions

- This Step 1 work is an architecture skeleton only.
- Streamlit is acceptable for the proof-of-concept UI.
- SQLite is acceptable for local prototype persistence and schema discussion.
- No production authentication is required in Step 1.
- No real email service is required in Step 1.
- HCP and haematologist are treated as the same portal role for this prototype skeleton.
- GSK Programme Admin is represented as `GSK Limited Viewer` to reinforce restricted access.
- The uploaded BRD is the source of truth for Step 1; conflicting future business decisions should supersede this document.

## Open Questions / Unclear Areas in the BRD

- Exact workflow states and allowed transitions are not final.
- Final reorder submission/approval model is not locked: pharmacist direct submission vs HCP review/approval.
- Evidence requirements for paid-dose confirmation are not confirmed.
- Detailed patient data fields are not final.
- Detailed notification triggers, recipients, message templates, and escalation rules are not final.
- GSK Programme Admin portal access is optional and subject to confirmation.
- Vial calculator business rules are in scope but not specified.
- Security controls, hosting, MFA, retention, and privacy implementation details require later design.
- Scarcity / stock approval handling is only described at a high level and remains outside formal portal workflow.
- There is a possible wording inconsistency: the document is labelled V1.2, while the summary refers to V1.1.

## Step 3 Addendum — Mock Role-Based Portal

Step 3 introduces a minimal mock role-based portal layer while keeping the project a proof-of-concept. The app now uses fake demo users stored in SQLite, Streamlit session state for the selected user, central role/permission configuration, and database-backed demo programme-record creation.

### Mock user/session handling

- `services/auth_service.py` stores the selected fake demo user in `st.session_state["current_user"]`.
- The sidebar renders a **Demo user** selector.
- No passwords, MFA, SSO, real credentials, or production identity provider integration are implemented.

### Role and permission design

Permissions are defined centrally in `config/roles.py`. Pages should call the auth/role helper functions rather than hardcoding authorisation decisions.

| Role | Step 3 permissions |
| --- | --- |
| HCP | Create records, view own records, submit placeholder permission. |
| Pharmacist | Create/prepare records and view own records. |
| CSP Admin | Create records, view all records, access CSP Admin, Audit Log, and Notification Log. |
| GSK Limited Viewer | View aggregate-only dashboard data. |

### Demo programme record creation

The existing `patients` table is treated as the prototype programme-record table. Step 3 intentionally collects only fake/demo operational fields: clinic patient code, site/clinic name, treating HCP name, and first paid-dose date. It does not collect patient name, DOB, NHI number, address, clinical details, or uploaded evidence.

### Audit and notification events

Creating a programme record now inserts:

- an `audit_log` row with `event_action = programme_record_created`, and
- a `notifications` row for CSP Admin with status `simulated`.

These events are local SQLite records only. No real email is sent.

### Intentionally deferred

Production authentication, production-grade authorisation, paid-dose verification, free-dose eligibility calculation, reorder workflow, vial calculator logic, evidence uploads, real email integration, and production privacy/security controls remain deferred to later steps.
