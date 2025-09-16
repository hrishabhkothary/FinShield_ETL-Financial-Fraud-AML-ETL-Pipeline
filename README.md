# FinShield_ETL

**Professional end-to-end ETL + Data Analysis project for financial fraud & AML detection**

**Project goal:** build a repeatable pipeline that simulates large-scale financial transaction data, ingests it into Snowflake (via Python or Informatica), transforms and stores it, then performs EDA and basic ML-based fraud detection using Python (pandas, numpy, matplotlib, seaborn).

---

## What industry problem this solves
- Detecting anomalous or fraudulent transactions in banking, payments and mobile-money systems (AML/anti-fraud). The pipeline demonstrates data ingestion, staging, transformation, and analytics required by Financial Crime teams and Data Engineering teams.
- Use cases: suspicious transaction detection, transaction monitoring, customer risk profiling, alerts feeding to downstream workflows.

---

## Architecture (high-level)
1. **Data sources**: public / synthetic large datasets (examples: Kaggle Credit Card Fraud dataset, PaySim synthetic mobile-money dataset, IEEE-CIS dataset). Use these for development or to seed a synthetic simulator.  
2. **Ingestion layer**:
   - **On‑prem / batch**: Informatica PowerCenter (use ODBC / PowerExchange for Snowflake).  
   - **Cloud / streaming**: Informatica Intelligent Cloud Services (IICS) using Snowflake connector (bulk load via Snowflake COPY).  
   - **Python alternative**: `snowflake-connector-python` + `write_pandas` or staged CSV + `COPY INTO`.
3. **Storage / Warehouse**: Snowflake (staging & curated schemas).  
4. **Transformation & ML**: Python (pandas, numpy) for feature engineering and scikit-learn for baseline models; visualizations with matplotlib & seaborn.
5. **Observability & Delivery**: simple Jupyter/python scripts produce reports and model artifacts.

---

## Contents of this repo
- `data_generator.py` — generate large synthetic transaction files (CSV).
- `etl/load_to_snowflake.py` — sample Python loader using `snowflake-connector-python` (create table, stage, COPY or write_pandas).
- `analysis/eda_and_model.py` — EDA pipeline + simple ML (train/test, model metrics, save model).
- `sql/schema.sql` — Snowflake DDL for `transactions` table + sample queries.
- `docs/informatica_powercenter.md` — step-by-step guidance to load data into Snowflake using PowerCenter (ODBC/PowerExchange).
- `docs/iics_snowflake.md` — step-by-step guidance to build an IICS mapping task and use the Snowflake connector.
- `requirements.txt` — Python libraries used.
- `.gitignore` — ignore data, env files.
- `README.md` — you are here.

---

## Where to get real / large datasets (suggestions)
- Kaggle **Credit Card Fraud Detection** (classic, ~284K rows) — great for modeling and EDA.  
- **PaySim** (synthetic mobile money simulator) — designed for fraud detection and can be scaled to millions of rows.  
- **IEEE-CIS Fraud Detection** (large, many features) — good for advanced feature engineering.



---

## Quickstart — environment & run steps (local machine, Windows or Linux)
1. **Prerequisites**
   - Python 3.9+ installed.
   - Optional: Snowflake account (trial or corporate). If you don't have Snowflake you can still run the data generator and local analysis.
   - Informatica PowerCenter (on-prem) or Informatica Intelligent Cloud (IICS) account to follow Informatica docs (not included as binaries here).
2. **Install Python packages**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows PowerShell or CMD
   pip install -r requirements.txt
   ```
3. **Generate synthetic data**
   ```bash
   python data_generator.py --rows 1000000 --out data/transactions.csv
   ```
4. **Load to Snowflake (Python example)**
   - Set env variables:
     - `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`
   - Run:
     ```bash
     python etl/load_to_snowflake.py --csv data/transactions.csv --table transactions
     ```
   - Or follow `docs/iics_snowflake.md` to perform the same with IICS, or `docs/informatica_powercenter.md` for PowerCenter.
5. **Run analysis & simple model**
   ```bash
   python analysis/eda_and_model.py --input data/transactions_sample.csv --out reports/
   ```

---

## How I designed the Python parts (what each tech does)
- **Python (pandas, numpy)** — data wrangling, feature engineering, and EDA. Use pandas for transformations (rollups, aggregations, time-window features).
- **matplotlib, seaborn** — charts for distribution, time-series patterns, correlation heatmaps.
- **SQL (Snowflake)** — persistent storage, heavy transformations (use `COPY INTO` + SQL transformations for scalable ops). Snowflake can also do light transformations during load. See Snowflake docs for `COPY INTO`.  
- **Informatica PowerCenter** — enterprise ETL for batch, complex transformations, and orchestration when running on-premise; uses ODBC/PowerExchange drivers to connect to Snowflake or an intermediate stage.  
- **Informatica Intelligent Cloud Services (IICS)** — cloud ETL; use Snowflake connector for high-throughput bulk ingestion using staged files + `COPY INTO`. (See IICS Snowflake connector docs in the chat reply for exact steps.)

---

## Explanation
1. **Problem statement**: "FinShield_ETL simulates and processes large-scale transactional data to detect anomalous behavior and potential financial crime (fraud/AML)."
2. **Architecture summary**: Explain ingestion (Informatica PowerCenter for on-prem batch; IICS for cloud), Snowflake as the analytical warehouse, and Python for analytics & modelling.
3. **Tech-by-tech responsibilities**:
   - Python — generation, cleaning, feature engineering, modelling, reporting.
   - SQL (Snowflake) — staging & heavy transformations (SQL-based enrichment, aggregation), materialized views.
   - Informatica PowerCenter — mapping & workflows for scheduled batch jobs; used when customers' systems are on-prem.
   - IICS — cloud mappings with Snowflake connector for streaming/bulk cloud loads.
4. **Key challenges & solutions**:
   - *Data volume* — use Snowflake stages and `COPY INTO` for efficient bulk loads; partition on date/time for downstream queries.
   - *Data imbalance (fraud is rare)* — use sampling, SMOTE or threshold tuning, and ensemble models; evaluate using precision/recall and PR-AUC.
   - *Explainability* — keep rule-based detectors (e.g., velocity checks) + ML models for hybrid detection.
5. **What you implemented**: walk through the repo files, show sample EDA plots, explain the features you engineered and why (e.g., transactions in last 1h, ratio to mean spend, device/location anomalies).
6. **How it maps to business value**: Faster detection, fewer false positives, auditable transformations in Snowflake and Informatica.


---

## Notes & next steps
- This scaffold contains Python code & docs. Real Informatica artifacts (exported mapplets/workflows) are not included since they require licensed tooling. Instead, step-by-step instructions are provided for building mappings and using Snowflake connectors.
- Use public datasets from Kaggle and PaySim to seed/validate the models.

---

