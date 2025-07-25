from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def debug_overdue_invoices_endpoint():
    print("Attempting to call /invoices/overdue endpoint...")
    response = client.get("/invoices/overdue")
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")
    return response

if __name__ == "__main__":
    debug_overdue_invoices_endpoint()