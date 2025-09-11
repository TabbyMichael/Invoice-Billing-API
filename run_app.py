import uvicorn
import os

print("--- Starting Server Runner ---")
print(f"Current Working Directory: {os.getcwd()}")

INVOICES_FILE = os.path.join('app', 'invoices.csv')
print(f"Checking for invoices file at path: {INVOICES_FILE}")

if os.path.exists(INVOICES_FILE):
    print("SUCCESS: Invoices file found.")
else:
    print("ERROR: Invoices file NOT found at that path.")
    print("Listing contents of 'app/' directory:")
    try:
        print(os.listdir('app'))
    except FileNotFoundError:
        print("'app/' directory does not exist.")

print("Attempting to start uvicorn...")
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
