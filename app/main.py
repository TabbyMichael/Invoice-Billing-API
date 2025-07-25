from fastapi import FastAPI, HTTPException, Request
from fastapi import FastAPI, HTTPException, Request
from typing import List, Optional
import time
import os

from .models import Invoice, InvoiceBase, Customer
from .data_loader import load_and_enhance_data
from .services import (
    get_invoices,
    get_invoice_by_number,
    get_invoices_by_customer,
    get_overdue_invoices,
    get_invoices_by_status,
    get_invoices_by_city,
    get_total_revenue,
    get_top_customers,
    get_top_products
)

# Load data
# Adjust the path to invoices.csv as it's now in the same directory as main.py
# but data_loader.py expects a path relative to the project root.
# So, we need to provide the full path from the project root.
INVOICES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'invoices.csv')
invoices_df = load_and_enhance_data(INVOICES_FILE)

app = FastAPI(
    title="Invoice & Billing API",
    description="A REST API for managing invoices and billing data.",
    version="1.0.0",
)

@app.get("/", summary="Root", description="Root endpoint of the API.")
async def read_root():
    return {"message": "Invoice & Billing API"}

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    if duration > 1.0:
        print(f"Slow request: {request.url} took {duration:.2f}s") # Consider using a proper logger
    return response

@app.get(
    "/invoices",
    response_model=List[Invoice],
    summary="Get all invoices",
    description="Returns a list of invoices, with optional filtering, pagination, and sorting.",
    response_description="A list of invoice objects"
)
def get_invoices_endpoint(
    status: Optional[str] = None,
    city: Optional[str] = None,
    sort_by: Optional[str] = "invoice_date",
    order: Optional[str] = "asc",
    limit: int = 20,
    offset: int = 0
):
    return get_invoices(status, city, sort_by, order, limit, offset)

@app.get(
    "/invoices/overdue",
    response_model=List[Invoice],
    summary="Get overdue invoices",
    description="Retrieve a list of all invoices that are currently overdue.",
    response_description="A list of overdue invoice objects"
)
def get_overdue_invoices_endpoint():
    overdue_invoices = get_overdue_invoices()
    if not overdue_invoices:
        return []
    return overdue_invoices

@app.get(
    "/invoices/{invoice_number}",
    response_model=Invoice,
    summary="Get invoice by number",
    description="Retrieve a single invoice by its unique invoice number.",
    response_description="An invoice object if found"
)
def get_invoice_by_number_endpoint(invoice_number: str):
    return get_invoice_by_number(invoice_number)

@app.get(
    "/customers/{customer_id}/invoices",
    response_model=List[Invoice],
    summary="Get invoices by customer ID",
    description="Retrieve a list of invoices associated with a specific customer ID.",
    response_description="A list of invoice objects for the given customer"
)
def get_invoices_by_customer_endpoint(customer_id: str):
    return get_invoices_by_customer(customer_id)

@app.get(
    "/invoices/status/{status}",
    response_model=List[Invoice],
    summary="Get invoices by status",
    description="Retrieve a list of invoices filtered by their status (e.g., 'paid', 'unpaid', 'overdue').",
    response_description="A list of invoice objects matching the specified status"
)
def get_invoices_by_status_endpoint(status: str):
    return get_invoices_by_status(status)

@app.get(
    "/invoices/city/{city}",
    response_model=List[Invoice],
    summary="Get invoices by city",
    description="Retrieve a list of invoices for a specific city.",
    response_description="A list of invoice objects for the specified city"
)
def get_invoices_by_city_endpoint(city: str):
    return get_invoices_by_city(city)

@app.get(
    "/analytics/total-revenue",
    summary="Get total revenue",
    description="Calculates and returns the total revenue from all invoices.",
    response_description="Total revenue from all invoices"
)
def get_total_revenue_endpoint():
    return {"total_revenue": get_total_revenue()}

@app.get(
    "/analytics/top-customers",
    response_model=List[Customer],
    summary="Get top customers",
    description="Retrieves a list of top customers based on their total spending.",
    response_description="A list of top customer objects"
)
def get_top_customers_endpoint(num_customers: int = 5):
    return get_top_customers(num_customers)

@app.get(
    "/analytics/top-products",
    summary="Get top products",
    description="Retrieves a list of top products based on their sales quantity.",
    response_description="A list of top product names and their quantities"
)
def get_top_products_endpoint(num_products: int = 5):
    return {"top_products": get_top_products(num_products)}