# Informatica PowerCenter -> Snowflake (guidance)
PowerCenter does not natively ship as a built-in Snowflake target in older versions. Recommended approaches:
1. **Use PowerExchange for Snowflake / ODBC**:
   - Install Snowflake ODBC driver on the PowerCenter Integration Service machines.
   - Create a Database Connection in PowerCenter (ODBC) pointing to Snowflake.
   - Create a Mapping: Source -> Expression/Lookup -> Target (Snowflake table).
   - For bulk loads, write to CSV (flat file) and use Snowflake `PUT` + `COPY INTO`, or use PowerExchange that supports bulk push.
2. **Use an intermediate cloud storage (S3/Azure)**:
   - PowerCenter writes CSVs to S3.
   - Use Snowflake `COPY INTO` from the S3 location.
3. **Best practice**:
   - For very large batches prefer staged file + COPY approach for throughput.
   - Keep transformations that are SQL-friendly inside Snowflake when possible (push-down).
Note: check your PowerCenter / PowerExchange version for Snowflake adapter support — consult vendor docs.
