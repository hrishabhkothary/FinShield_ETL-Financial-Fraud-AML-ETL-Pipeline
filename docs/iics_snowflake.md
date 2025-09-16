# IICS (Informatica Intelligent Cloud Services) -> Snowflake (guidance)
1. Create a new Connection in IICS (Administrator -> Connections -> New):
   - Choose Snowflake or Snowflake Cloud Data Warehouse V2 connector.
   - Provide account, user, password, warehouse, database, schema.
2. Create a Data Integration mapping:
   - Source -> Transformation(s) -> Target (Snowflake).
   - When using the Snowflake connector, choose the 'Bulk' option where available to enable staging + COPY (faster).
3. Use mapping tasks and schedule using IICS scheduler.
4. For large-scale loads, IICS Snowflake connector will create temporary files and use Snowflake COPY under the hood.
Refer to the official IICS Snowflake connector documentation to match your IICS release and connector version.
