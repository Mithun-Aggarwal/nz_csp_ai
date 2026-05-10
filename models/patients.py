"""Programme record model for the Step 3 prototype.

Do not use real patient data in this prototype. ``clinic_patient_code`` is a
fake/demo operational identifier only.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PatientProgramRecord:
    """Minimal database-backed demo programme record."""

    id: Optional[int]
    clinic_patient_code: str
    site_name: str
    treating_hcp_name: str
    first_paid_dose_date: str
    current_status: str
    created_by_user_id: Optional[int]
    created_by_role: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
