"""Workflow state placeholders for the CSP lifecycle.

Future work should replace these constants with validated transitions,
role-specific permissions, and database-backed workflow history.
"""

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class WorkflowState:
    """Describes a draft workflow state."""

    key: str
    label: str
    description: str


WORKFLOW_STATES = [
    WorkflowState("draft_prepared_by_pharmacist", "Draft prepared by pharmacist", "Record started by pharmacist."),
    WorkflowState("draft_created_by_hcp", "Draft created by HCP", "Record started by haematologist/HCP."),
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


def list_state_labels() -> list[str]:
    """Return labels for display in placeholder pages."""

    return [state.label for state in WORKFLOW_STATES]
