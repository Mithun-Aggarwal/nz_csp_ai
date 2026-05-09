"""Patient programme record placeholders.

Do not use real patient data in this prototype. The clinic patient code is the
preferred operational identifier described in the BRD.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class PatientProgramRecord:
    """Minimal longitudinal CSP programme record."""

    clinic_patient_code: str
    current_status: str
    first_paid_dose_date: date | None = None
    free_dose_start_date: date | None = None
    free_dose_end_date: date | None = None
