from .data_loader import load_and_enhance_data
from fastapi import HTTPException
from .models import Invoice, Customer
from datetime import datetime
import pandas as pd
from typing import Optional

# Load data once at startup
import os
INVOICES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'invoices.csv')
invoices_df = load_and_enhance_data(INVOICES_FILE)

# Ensure 'due_date' is in datetime format for comparison
invoices_df['due_date'] = pd.to_datetime(invoices_df['due_date'])

def get_invoices(
    status: Optional[str] = None,
    city: Optional[str] = None,
    sort_by: Optional[str] = "invoice_date",
    order: Optional[str] = "asc",
    limit: int = 20,
    offset: int = 0
):
    df = invoices_df.copy()

    if status:
        df = df[df["status"] == status]
    if city:
        df = df[df["city"] == city]

    # Ensure sort_by column exists to prevent KeyError
    if sort_by not in df.columns:
        sort_by = "invoice_date" # Default to invoice_date if column not found

    df = df.sort_values(by=sort_by, ascending=(order == "asc"))
    
    invoice_columns = [
        'first_name', 'last_name', 'email', 'product_id', 'qty', 'amount', 'invoice_date', 'address', 'city',
        'stock_code', 'job', 'invoice_number', 'due_date', 'status', 'customer_id', 'name', 'country'
    ]
    df['due_date'] = df['due_date'].dt.strftime('%Y-%m-%d')
    return df[invoice_columns].iloc[offset:offset + limit].to_dict(orient="records")


def get_invoice_by_number(invoice_number: str):
    invoice = invoices_df[invoices_df['invoice_number'] == invoice_number]
    if invoice.empty:
        raise HTTPException(status_code=404, detail="Invoice not found")
    invoice_dict = invoice.iloc[0].to_dict()
    invoice_dict['due_date'] = invoice_dict['due_date'].strftime('%Y-%m-%d')
    return invoice_dict


def get_invoices_by_customer(customer_id: str):
    customer_invoices = invoices_df[invoices_df['customer_id'] == customer_id]
    return customer_invoices.to_dict(orient="records")


def get_overdue_invoices():
    today = datetime.now().date()
    overdue_df = invoices_df[(invoices_df['status'] == 'unpaid') & (invoices_df['due_date'].dt.date < today)]
    overdue_df['due_date'] = overdue_df['due_date'].dt.strftime('%Y-%m-%d')
    return overdue_df.to_dict(orient="records")


def get_invoices_by_status(status: str):
    filtered_df = invoices_df[invoices_df['status'] == status]
    return filtered_df.to_dict(orient="records")


def get_invoices_by_city(city: str):
    filtered_df = invoices_df[invoices_df['city'] == city]
    return filtered_df.to_dict(orient="records")


def get_total_revenue():
    return invoices_df['amount'].sum()


def get_top_customers(num_customers: int = 5):
    customer_revenue = invoices_df.groupby('customer_id')['amount'].sum().nlargest(num_customers)
    top_customers_data = []
    for cust_id, revenue in customer_revenue.items():
        customer_info = invoices_df[invoices_df['customer_id'] == cust_id].iloc[0]
        top_customers_data.append({
            "customer_id": cust_id,
            "name": customer_info['name'],
            "email": customer_info['email'],
            "total_spent": revenue
        })
    return top_customers_data


def get_top_products(num_products: int = 5):
    product_quantity = invoices_df.groupby('product_id')['qty'].sum().nlargest(num_products)
    return product_quantity.to_dict()