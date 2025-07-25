from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Invoice & Billing API"}

def test_get_invoices():
    response = client.get("/invoices")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_invoices_with_status_filter():
    response = client.get("/invoices?status=paid")
    assert response.status_code == 200
    assert all(invoice['status'] == 'paid' for invoice in response.json())

def test_get_invoices_with_city_filter():
    # Assuming 'New York' is a city in your invoices.csv
    response = client.get("/invoices?city=New York")
    assert response.status_code == 200
    assert all(invoice['city'] == 'New York' for invoice in response.json())

def test_get_invoices_with_pagination():
    response = client.get("/invoices?limit=5&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_get_invoices_with_sorting():
    response = client.get("/invoices?sort_by=amount&order=desc")
    assert response.status_code == 200
    amounts = [invoice['amount'] for invoice in response.json()]
    assert all(amounts[i] >= amounts[i+1] for i in range(len(amounts) - 1))

def test_get_invoice_by_number():
    # Get an invoice number from the /invoices endpoint
    invoices_response = client.get("/invoices")
    assert invoices_response.status_code == 200
    invoices = invoices_response.json()
    assert len(invoices) > 0
    invoice_number = invoices[0]['invoice_number']
    
    response = client.get(f"/invoices/{invoice_number}")
    assert response.status_code == 200
    assert response.json()['invoice_number'] == invoice_number

def test_get_invoice_by_number_not_found():
    response = client.get("/invoices/NONEXISTENT")
    assert response.status_code == 404
    assert response.json() == {"detail": "Invoice not found"}

def test_get_overdue_invoices():
    response = client.get("/invoices/overdue")
    assert response.status_code == 200
    # Further assertions can be made if you have control over test data to ensure overdue invoices exist

def test_get_total_revenue():
    response = client.get("/analytics/total-revenue")
    assert response.status_code == 200
    assert "total_revenue" in response.json()
    assert isinstance(response.json()["total_revenue"], (int, float))

def test_get_top_customers():
    response = client.get("/analytics/top-customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "customer_id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "total_spent" in response.json()[0]

def test_get_top_products():
    response = client.get("/analytics/top-products")
    assert response.status_code == 200
    assert "top_products" in response.json()
    assert isinstance(response.json()["top_products"], dict)
    assert len(response.json()["top_products"]) > 0