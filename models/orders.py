"""Order and paid-dose model placeholders."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Order:
    """Manual order/reorder transaction placeholder."""

    patient_id: int
    order_type: str
    order_status: str = "draft"
    requested_date: Optional[date] = None


@dataclass
class PaidDoseRecord:
    """Paid-dose attestation placeholder."""

    patient_id: int
    dose_number: int
    dose_date: Optional[date] = None
    attestation_status: str = "pending"
