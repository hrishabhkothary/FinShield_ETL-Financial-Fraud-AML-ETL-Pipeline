"""data_generator.py
Generates synthetic transaction CSVs at scale for fraud detection experiments.
Usage:
    python data_generator.py --rows 1000000 --out data/transactions.csv
"""
import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import random

def generate_transactions(n_rows=100000, start_date='2024-01-01'):
    np.random.seed(42)
    random.seed(42)
    start = datetime.fromisoformat(start_date)
    timestamps = [start + timedelta(seconds=int(x)) for x in np.random.exponential(scale=60, size=n_rows).cumsum()]
    customer_ids = np.random.randint(10000, 200000, size=n_rows)
    merchant_ids = np.random.randint(1000, 50000, size=n_rows)
    amounts = np.round(np.random.exponential(scale=50, size=n_rows), 2)
    types = np.random.choice(['PAYMENT','TRANSFER','CASH_OUT','DEBIT','CREDIT'], size=n_rows, p=[0.5,0.2,0.15,0.1,0.05])
    is_fraud = np.zeros(n_rows, dtype=int)
    # Inject some fraud patterns
    idx = np.random.choice(n_rows, size=max(10, n_rows//5000), replace=False)
    is_fraud[idx] = 1
    df = pd.DataFrame({
        'transaction_id': [f'TX{1000000+i}' for i in range(n_rows)],
        'event_time': timestamps,
        'customer_id': customer_ids,
        'merchant_id': merchant_ids,
        'tx_amount': amounts,
        'tx_type': types,
        'is_fraud': is_fraud
    })
    # Add a few engineered-ish columns
    df['hour'] = df['event_time'].dt.hour
    df['day'] = df['event_time'].dt.date
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=100000, help='number of rows to generate')
    parser.add_argument('--out', type=str, default='data/transactions.csv', help='output csv path')
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df = generate_transactions(args.rows)
    df.to_csv(args.out, index=False)
    print(f"Wrote {len(df)} rows to {args.out}")

if __name__ == '__main__':
    main()
