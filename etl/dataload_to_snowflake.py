"""etl/load_to_snowflake.py (UPDATED)

Convenience loader for FinShield_ETL.
- Defaults: --csv -> data/transactions_sample.csv, --table -> TRANSACTIONS
- Loads environment variables from .env via python-dotenv
- Auto-creates a Snowflake table if it doesn't exist (inferring column types from the DataFrame)
- Uses write_pandas for medium-size loads

Usage:
    python etl/load_to_snowflake.py  # uses defaults
    python etl/load_to_snowflake.py --csv data/myfile.csv --table my_table

Make sure .env contains SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ACCOUNT, and optionally SNOWFLAKE_WAREHOUSE, SNOWFLAKE_DATABASE, SNOWFLAKE_SCHEMA.
"""

import os
import argparse
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

def get_env(name, required=False, default=None):
    val = os.environ.get(name, default)
    if required and (val is None or val == ""):
        raise RuntimeError(f"Required environment variable {name} is not set. Please add it to your .env or env.")
    return val

def connect():
    user = get_env('SF_USERNAME', required=True)
    password = get_env('SF_PASSWORD', required=True)
    account = get_env('SF_ACCOUNT_IDENTIFIER', required=True)
    warehouse = get_env('COMPUTE_WH')
    database = get_env('FINSHIELD_DB')
    schema = get_env('PUBLIC')

    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        client_session_keep_alive=True
    )
    return conn

# Map pandas dtype to Snowflake SQL types
def sf_type_from_series(s: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(s.dtype):
        return 'NUMBER'
    if pd.api.types.is_float_dtype(s.dtype):
        return 'FLOAT'
    if pd.api.types.is_bool_dtype(s.dtype):
        return 'BOOLEAN'
    if pd.api.types.is_datetime64_any_dtype(s.dtype):
        return 'TIMESTAMP_NTZ'
    # fallback for object / string / mixed
    return 'STRING'

def create_table_if_not_exists(conn, table_name: str, df: pd.DataFrame):
    # build CREATE TABLE statement from df columns and inferred types
    cols = []
    for col in df.columns:
        sf_type = sf_type_from_series(df[col])
        # sanitize column names (simple): remove spaces, keep underscores
        colname = str(col).strip().replace(' ', '_')
        cols.append(f'"{colname.upper()}" {sf_type}')

    ddl = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)});"
    cs = conn.cursor()
    try:
        cs.execute(ddl)
        print(f"Ensured table exists: {table_name}")
    finally:
        cs.close()


def load_via_write_pandas(conn, df: pd.DataFrame, table_name: str):
    # write_pandas expects the table name (it will uppercase)
    print('Loading dataframe via write_pandas (suitable for medium-sized uploads)...')
    success, nchunks, nrows, _ = write_pandas(conn, df, table_name)
    print(f"write_pandas success={success} nchunks={nchunks} nrows={nrows}")


def main():
    parser = argparse.ArgumentParser(description='Load a CSV into Snowflake (convenience wrapper).')
    parser.add_argument('--csv', default='data/transactions_sample.csv', help='Path to CSV file (default: data/transactions_sample.csv)')
    parser.add_argument('--table', default='TRANSACTIONS', help='Target Snowflake table name (default: TRANSACTIONS)')
    args = parser.parse_args()

    csv_path = args.csv
    table_name = args.table

    if not os.path.exists(csv_path):
        raise SystemExit(f"CSV file not found: {csv_path} - please check the path or generate the sample using data_generator.py")

    print(f"Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path, parse_dates=True, infer_datetime_format=True)

    # Basic cleanup: strip column names
    df.columns = [c.strip() for c in df.columns]

    # Connect and ensure table
    try:
        conn = connect()
    except Exception as e:
        raise SystemExit(f"Failed to connect to Snowflake: {e}")

    # If the environment provided a database+schema, table_name can be simple; otherwise user can pass DB.SCHEMA.TABLE
    # For safety, keep the table_name as provided
    create_table_if_not_exists(conn, table_name, df)

    # Load data
    try:
        load_via_write_pandas(conn, df, table_name)
    except Exception as e:
        print('Error during write_pandas load:', e)
        print('Consider staging the CSV to an internal stage and using COPY INTO for very large files.')
    finally:
        conn.close()

if __name__ == '__main__':
    main()
