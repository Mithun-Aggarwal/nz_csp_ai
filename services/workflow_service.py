"""Workflow and programme-record helpers for the Step 3 prototype."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Dict, List

from config.roles import ROLE_HCP, ROLE_PHARMACIST
from database.db import get_connection, rows_to_dicts
from services.audit_service import create_audit_event
from services.notification_service import create_programme_record_notification

STATUS_DRAFT_CREATED_BY_HCP = "draft_created_by_hcp"
STATUS_DRAFT_PREPARED_BY_PHARMACIST = "draft_prepared_by_pharmacist"


@dataclass(frozen=True)
class WorkflowState:
    """Describes a draft workflow state."""

    key: str
    label: str
    description: str


WORKFLOW_STATES = [
    WorkflowState(STATUS_DRAFT_PREPARED_BY_PHARMACIST, "Draft prepared by pharmacist", "Record started by pharmacist."),
    WorkflowState(STATUS_DRAFT_CREATED_BY_HCP, "Draft created by HCP", "Record started by haematologist/HCP."),
    WorkflowState("submitted_for_hcp_approval", "Submitted for HCP approval", "Awaiting HCP review/submission."),
    WorkflowState("submitted_for_csp_verification", "Submitted for CSP verification", "Awaiting CSP Admin verification."),
    WorkflowState("paid_doses_pending_confirmation", "Paid doses pending confirmation", "Awaiting first three paid-dose attestations."),
    WorkflowState("paid_doses_confirmed", "Paid doses confirmed", "First three privately funded doses confirmed."),
    WorkflowState("eligible_for_free_doses", "Eligible for free doses", "Eligibility confirmed; free-dose period can begin."),
    WorkflowState("active_free_dose_period", "Active free-dose period", "Patient is in the free-dose period."),
    WorkflowState("free_dose_period_expiring", "Free-dose period expiring", "Free-dose period is approaching expiry."),
    WorkflowState("reset_to_paid_pathway", "Reset to paid pathway", "One-year period ended; cycle resets."),
    WorkflowState("closed_or_discontinued", "Closed or discontinued", "Record is no longer active."),
]


def calculate_free_dose_end_date(first_paid_dose_date: date) -> date:
    """Draft calculation for the one-year period from first paid dose date."""

    return first_paid_dose_date + timedelta(days=365)


def list_state_labels() -> List[str]:
    """Return labels for display in placeholder pages."""

    return [state.label for state in WORKFLOW_STATES]


def _default_status_for_role(role: str) -> str:
    """Return the Step 3 default draft status for a creator role."""

    if role == ROLE_PHARMACIST:
        return STATUS_DRAFT_PREPARED_BY_PHARMACIST
    return STATUS_DRAFT_CREATED_BY_HCP


def create_programme_record(
    clinic_patient_code: str,
    site_name: str,
    treating_hcp_name: str,
    first_paid_dose_date: date,
    current_user: Dict[str, Any],
) -> int:
    """Create a minimal demo programme record, audit event, and notification."""

    status = _default_status_for_role(current_user.get("role", ROLE_HCP))
    dose_date_text = first_paid_dose_date.isoformat()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO patients (
                clinic_patient_code,
                site_name,
                treating_hcp_name,
                first_paid_dose_date,
                current_status,
                created_by_user_id,
                created_by_role,
                haematologist_user_id,
                pharmacist_user_id,
                site_code
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                clinic_patient_code.strip(),
                site_name.strip(),
                treating_hcp_name.strip(),
                dose_date_text,
                status,
                current_user.get("id"),
                current_user.get("role"),
                current_user.get("id") if current_user.get("role") == ROLE_HCP else None,
                current_user.get("id") if current_user.get("role") == ROLE_PHARMACIST else None,
                site_name.strip(),
            ),
        )
        record_id = int(cursor.lastrowid)

    create_audit_event(
        event_action="programme_record_created",
        entity_type="programme_record",
        entity_id=str(record_id),
        performed_by_user=current_user,
        details="Demo programme record %s created with status %s." % (record_id, status),
    )
    create_programme_record_notification()
    return record_id


def list_programme_records_for_user(current_user: Dict[str, Any]) -> List[Dict[str, Any]]:
    """List records created by a specific demo user."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                clinic_patient_code,
                site_name,
                treating_hcp_name,
                first_paid_dose_date,
                current_status,
                created_by_user_id,
                created_by_role,
                created_at,
                updated_at
            FROM patients
            WHERE created_by_user_id = ?
            ORDER BY datetime(created_at) DESC, id DESC
            """,
            (current_user.get("id"),),
        ).fetchall()
    return rows_to_dicts(rows)


def list_all_programme_records() -> List[Dict[str, Any]]:
    """List all demo programme records."""

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                p.id,
                p.clinic_patient_code,
                p.site_name,
                p.treating_hcp_name,
                p.first_paid_dose_date,
                p.current_status,
                p.created_by_role,
                u.display_name AS created_by,
                p.created_at,
                p.updated_at
            FROM patients p
            LEFT JOIN users u ON u.id = p.created_by_user_id
            ORDER BY datetime(p.created_at) DESC, p.id DESC
            """
        ).fetchall()
    return rows_to_dicts(rows)


def get_programme_record_counts() -> Dict[str, Any]:
    """Return aggregate counts for admin and restricted dashboards."""

    with get_connection() as connection:
        total_row = connection.execute("SELECT COUNT(*) AS total FROM patients").fetchone()
        status_rows = connection.execute(
            """
            SELECT current_status, COUNT(*) AS count
            FROM patients
            GROUP BY current_status
            ORDER BY current_status
            """
        ).fetchall()
    return {
        "total": int(total_row["total"]),
        "by_status": rows_to_dicts(status_rows),
    }
