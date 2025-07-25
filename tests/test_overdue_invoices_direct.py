import pytest
from app.services import get_overdue_invoices

def test_get_overdue_invoices_direct():
    overdue_invoices = get_overdue_invoices()
    print(f"[test_overdue_invoices_direct] Overdue invoices: {overdue_invoices}")
    assert isinstance(overdue_invoices, list)
    # Further assertions can be added here based on expected data