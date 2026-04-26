# 📈 Stock Market Data Engineering

A daily data pipeline that collects stock market data from Apple (AAPL) and NVIDIA (NVDA), applies financial calculations, and stores the results using a **Medallion Architecture** with AWS S3 (Bronze) and Snowflake (Silver).

---

## 🏗️ Architecture

```
yfinance API
     │
     ▼
[ Bronze Layer ]  ──── Raw data stored as Parquet in AWS S3
     │
     ▼
[ Silver Layer ]  ──── Cleaned + enriched data stored in Snowflake
     │
     ▼
[ Orchestration ] ──── Apache Airflow (Docker) runs daily at 20:25 UTC
```

---

## ⚙️ Tech Stack

| Tool | Role |
|------|------|
| `yfinance` | Stock data ingestion (AAPL, NVDA) |
| `pandas` / `numpy` | Data transformation and financial calculations |
| `AWS S3` | Bronze layer — raw data storage |
| `boto3` | AWS S3 integration |
| `Snowflake` | Silver layer — cleaned and enriched data |
| `snowflake-connector-python` | Snowflake integration |
| `Apache Airflow` | Pipeline orchestration |
| `Docker` / `Docker Compose` | Containerized infrastructure |
| `Jupyter Notebook` | Pipeline logic via `nbconvert` |

---

## 📊 Data & Transformations

The pipeline collects daily OHLCV data for each ticker and adds the following calculated columns:

- `variation_past_day` — price variation compared to the previous day
- `percent_variation_past_day` — percentage variation compared to the previous day
- `gap_past_day` — gap between previous close and current open
- `flag_day` — classification of the trading day based on behavior
- `insert_date` — timestamp of when the record was inserted

---

## 🗃️ Snowflake Schema

```sql
DATABASE: ace_low
SCHEMA: stocks
TABLE: stock_market

Columns:
  key                        INTEGER PRIMARY KEY
  date                       DATETIME NOT NULL
  ticker                     STRING
  open                       FLOAT
  low                        FLOAT
  high                       FLOAT
  close                      FLOAT
  stock_splits               FLOAT
  dividends                  FLOAT
  volume                     FLOAT
  variation_past_day         FLOAT
  percent_variation_past_day FLOAT
  gap_past_day               FLOAT
  flag_day                   STRING
  insert_date                DATETIME
```

---

## 🚀 How to Run

### Prerequisites

- Docker & Docker Compose installed
- AWS account with S3 bucket
- Snowflake account

### 1. Clone the repository

```bash
git clone https://github.com/Guilherme-Software/Stock_Market.git
cd Stock_Market/airflow-docker
```

### 2. Configure environment variables

Create a `.env` file based on the example below:

```env
AIRFLOW_UID=50000

# AWS
ACCESS_KEY=your_aws_access_key
SECRET_KEY=your_aws_secret_key

# Snowflake
USER_SNOW=your_snowflake_user
PASSWORD_SNOW=your_snowflake_password
ACCOUNT_SNOW=your_snowflake_account
```

### 3. Start the containers

```bash
docker compose up --build -d
```

### 4. Access the Airflow UI

Open [http://localhost:8080](http://localhost:8080) in your browser.

Default credentials:
- **User:** `airflow`
- **Password:** `airflow`

### 5. Trigger the DAG

The DAG `stocks_pipeline` runs automatically every day at **20:25 UTC**.
To trigger it manually, click the ▶ button in the Airflow UI.

---

## 📁 Project Structure

```
Stock_Market/
├── airflow-docker/
│   ├── dags/
│   │   ├── main.ipynb        # Pipeline logic (Jupyter Notebook)
│   │   └── stocks_dag.py     # Airflow DAG definition
│   ├── Dockerfile            # Custom Airflow image with dependencies
│   ├── docker-compose.yaml   # Full Airflow stack
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment variables template
└── README.md
```

---

## 🔒 Security

- Never commit your `.env` file — it contains sensitive credentials.
- The `.env` file need to be listed in `.gitignore`.