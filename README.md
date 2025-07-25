# Invoice & Billing API

A REST API for managing invoices and billing data, built with FastAPI.

## Project Structure

```
invoice_api/
├── app/
│   ├── main.py          # FastAPI app with endpoints
│   ├── models.py        # Pydantic schemas
│   ├── services.py      # Business logic and filtering
│   ├── data_loader.py   # CSV loader and field simulation
│   └── invoices.csv     # Your mock dataset
├── requirements.txt     # FastAPI, Pandas, Uvicorn
└── README.md            # Setup instructions and API guide
```

## Features

This API provides the following functionalities:

- **Data Enhancement**: Processes `invoices.csv` by adding `invoice_number`, `due_date`, `status`, `customer_id`, `name`, and `country` fields. Dates are formatted to YYYY-MM-DD, and missing values are handled.
- **Core Endpoints**:
    - List all invoices with pagination (`GET /invoices`)
    - Get a single invoice by number (`GET /invoices/{invoice_number}`)
    - List invoices by customer (`GET /customers/{customer_id}/invoices`)
    - List due invoices (`GET /invoices/due`)
    - Filter invoices by status (`GET /invoices/status/{status}`)
    - Get invoices by city (`GET /city/{city}/invoices`)
- **Analytics Endpoints**:
    - Total revenue (`GET /analytics/total-revenue`)
    - Top customers (`GET /analytics/top-customers`)
    - Top products (`GET /analytics/top-products`)

## Setup Instructions

Follow these steps to set up and run the Invoice & Billing API locally:

### 1. Clone the repository (if you haven't already)

```bash
git clone https://github.com/your-username/invoice_api.git
cd invoice_api
```

### 2. Install Dependencies

It is highly recommended to use a virtual environment.

```bash
python -m venv venv
.\venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

**Troubleshooting `pandas` or `pydantic` installation issues:**
If you encounter errors related to `pandas` or `pydantic` during installation (e.g., "Could not parse vswhere.exe output" or "Microsoft Visual C++ 14.0 or greater is required"), you might need to install Visual C++ build tools.

For Windows, download and install "Build Tools for Visual Studio" from the official Microsoft website. During installation, select the "Desktop development with C++" workload.

After installing the build tools, try running `pip install -r requirements.txt` again.

### 3. Run the Application

Navigate to the root directory of the project and run the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

This will start the development server, typically accessible at `http://127.0.0.1:8000`.

### 4. Access the API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:

[http://127.0.0.1:8000/docs](http://127.00.1:8000/docs)

Here you can test all the available endpoints.

## API Guide

All endpoints return JSON responses.

### Invoices

- **GET /invoices**
    - **Description**: List all invoices with pagination.
    - **Query Parameters**:
        - `limit` (int, default: 10): Number of invoices to return.
        - `offset` (int, default: 0): Number of invoices to skip.

- **GET /invoices/{invoice_number}**
    - **Description**: Get full details of a single invoice by its unique invoice number.
    - **Path Parameters**:
        - `invoice_number` (str): The unique invoice number (e.g., `INV-00001`).

- **GET /customers/{customer_id}/invoices**
    - **Description**: List all invoices associated with a specific customer.
    - **Path Parameters**:
        - `customer_id` (str): The unique ID of the customer.

- **GET /invoices/due**
    - **Description**: List all unpaid and overdue invoices.

- **GET /invoices/status/{status}**
    - **Description**: Filter invoices by their payment status.
    - **Path Parameters**:
        - `status` (str): The status to filter by. Can be `paid` or `unpaid`.

- **GET /city/{city}/invoices**
    - **Description**: Get all invoices issued from a specific city.
    - **Path Parameters**:
        - `city` (str): The name of the city.

### Analytics

- **GET /analytics/total-revenue**
    - **Description**: Get the sum of all invoice amounts.

- **GET /analytics/top-customers**
    - **Description**: Get a list of top customers ranked by their total spending.
    - **Query Parameters**:
        - `limit` (int, default: 5): Number of top customers to return.

- **GET /analytics/top-products**
    - **Description**: Get a list of top products ranked by the total quantity sold.
    - **Query Parameters**:
        - `limit` (int, default: 5): Number of top products to return.

## Data Source

The API uses `app/invoices.csv` as its data source. This file is processed and enhanced upon application startup.

## Running Tests

Unit and integration tests are available to ensure the API's functionality and reliability. Tests are written using `pytest`.

### How to Run Tests

Navigate to the root directory of the project and run `pytest`:

```bash
pytest
```

To run a specific test file, you can specify its path:

```bash
pytest tests/test_main.py
```

### Test Coverage

The test suite includes:

-   **Endpoint Tests**: Verifies the correct behavior of various API endpoints, including `/invoices`, `/invoices/{invoice_number}`, and `/invoices/overdue`.
-   **Filtering, Pagination, and Sorting**: Ensures that query parameters for filtering, pagination, and sorting work as expected.
-   **Overdue Detection Logic**: Validates the logic for identifying overdue invoices.
-   **Error Handling**: Checks for proper 404 error handling for unknown invoice numbers and other invalid requests.#   I n v o i c e - B i l l i n g - A P I  
 