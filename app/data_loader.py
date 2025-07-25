import pandas as pd
import hashlib
import random
from datetime import datetime, timedelta
from functools import lru_cache


@lru_cache(maxsize=1)
def load_and_enhance_data(file_path: str):
    df = pd.read_csv(file_path)

    # Data Enhancement
    df['invoice_number'] = [f'INV-{i+1:05d}' for i in range(len(df))]
    df['due_date'] = pd.to_datetime(df['invoice_date'], format='%d/%m/%Y') + timedelta(days=30)
    df['status'] = [random.choice(['paid', 'unpaid']) for _ in range(len(df))]
    df['customer_id'] = df['email'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:10])
    df['name'] = df['first_name'] + ' ' + df['last_name']
    df['country'] = 'USA' # Static for now, can be mapped from city if needed

    # Format dates as YYYY-MM-DD
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    df['due_date'] = df['due_date'].dt.strftime('%Y-%m-%d')

    # Ensure no NaNs or nulls (fill with empty string for object columns, 0 for numeric)
    df = df.fillna('')

    return df