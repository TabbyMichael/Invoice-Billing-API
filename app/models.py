from pydantic import BaseModel
from typing import List

class InvoiceBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    product_id: int
    qty: int
    amount: float
    invoice_date: str
    address: str
    city: str
    stock_code: int
    job: str

class Invoice(InvoiceBase):
    invoice_number: str
    due_date: str
    status: str
    customer_id: str
    name: str
    country: str

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    total_spent: float