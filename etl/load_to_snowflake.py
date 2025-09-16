"""etl/load_to_snowflake.py
Simple loader that either uses write_pandas or stages CSV and uses COPY INTO for large files.
Requires env vars:
  SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA
Usage:
  python etl/load_to_snowflake.py --csv data/transactions.csv --table transactions
"""
import os
import argparse
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd

def connect():
    return snowflake.connector.connect(
        user=os.environ['SF_USERNAME'],
        password=os.environ['SF_Password'],
        account=os.environ['SF_ACCOUNT_Identifier'],
        warehouse=os.environ.get('COMPUTE_WH'),
        database=os.environ.get('FINSHIELD_DB'),
        schema=os.environ.get('PUBLIC'),
        client_session_keep_alive=True
    )

def ensure_table(conn, table_name):
    cs = conn.cursor()
    try:
        cs.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            transaction_id STRING,
            event_time TIMESTAMP_NTZ,
            customer_id NUMBER,
            merchant_id NUMBER,
            tx_amount FLOAT,
            tx_type STRING,
            is_fraud NUMBER,
            hour NUMBER,
            day DATE
        )""")
    finally:
        cs.close()

def load_via_write_pandas(conn, df, table_name):
    # write_pandas is convenient for medium-sized DataFrames
    success, nchunks, nrows, _ = write_pandas(conn, df, table_name.upper())
    print(f"write_pandas success={success} nchunks={nchunks} nrows={nrows}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True)
    parser.add_argument('--table', default='transactions')
    args = parser.parse_args()
    df = pd.read_csv(args.csv, parse_dates=['event_time'])
    conn = connect()
    ensure_table(conn, args.table)
    # For example purposes we'll use write_pandas. For very large files, stage + COPY is preferred.
    load_via_write_pandas(conn, df, args.table)
    conn.close()

if __name__ == '__main__':
    main()
