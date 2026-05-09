"""Order and paid-dose model placeholders."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Order:
    """Manual order/reorder transaction placeholder."""

    patient_id: int
    order_type: str
    order_status: str = "draft"
    requested_date: date | None = None


@dataclass
class PaidDoseRecord:
    """Paid-dose attestation placeholder."""

    patient_id: int
    dose_number: int
    dose_date: date | None = None
    attestation_status: str = "pending"
