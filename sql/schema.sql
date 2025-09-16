-- sql/schema.sql
CREATE OR REPLACE TABLE transactions (
  transaction_id STRING,
  event_time TIMESTAMP_NTZ,
  customer_id NUMBER,
  merchant_id NUMBER,
  tx_amount FLOAT,
  tx_type STRING,
  is_fraud NUMBER,
  hour NUMBER,
  day DATE
);

-- Example: create a named internal stage and load from it
-- PUT file://transactions.csv @%transactions;
-- COPY INTO transactions FROM @%transactions FILE_FORMAT = (TYPE=CSV FIELD_OPTIONALLY_ENCLOSED_BY='"') ON_ERROR='CONTINUE';
