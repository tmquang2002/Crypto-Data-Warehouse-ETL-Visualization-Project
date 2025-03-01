# Crypto Data Warehouse ETL & Visualization Project
<img src="https://i.ibb.co/WWh7JHGS/aa.png" alt="NCHMF" width="500"/>


## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [Setup Instructions](#setup-instructions)
- [Data Pipeline](#data-pipeline)
- [Usage](#usage)
- [Visualizations](#visualizations)
- [Conclusion](#conclusion)
- [Future Direction](#future-direction)

## Introduction

Crypto Data Warehouse ETL & Visualization Project is a complete system for collecting, processing, storing, and visualizing cryptocurrency market data. The data is fetched from the CoinGecko API, stored as CSV files on MinIO, then transformed and loaded into a PostgreSQL database following the Star Schema model with dimension and fact tables. Finally, the data is visualized and analyzed using Metabase.

## Technologies Used
- **Python**: Fetching and processing data from CoinGecko API.
- **MinIO**: Object storage for raw CSV files.
- **PostgreSQL**: Data warehouse with Star Schema design.
- **Metabase**: Data visualization and dashboard creation.
- **Docker Compose**: Orchestrates services like PostgreSQL, MinIO, and Metabase.
- **Airflow (Optional)**: Automates and schedules ETL jobs.

## System Architecture

### 1. Data Collection
- **Data Source**: CoinGecko API providing information on cryptocurrencies like Bitcoin, Ethereum, USDC, Tether, Binance Coin, Ripple, Cardano, Dogecoin, Solana, and Tron.
- **Crawl & Extract**: A Python script fetches API data and saves it as CSV files.
- **Storage on MinIO**: CSV files are uploaded to MinIO with a time-based directory structure (e.g., `2025/02/28/10-10-14.csv`).

### 2. ETL & Data Warehouse Process

**Extract (Data Extraction):**
- The system periodically scans MinIO directories to check for newly uploaded CSV files.
- These files contain cryptocurrency market data collected from the CoinGecko API.

**Transform (Data Transformation):**
- Raw CSV data is cleaned and standardized to fit the Star Schema model of the data warehouse.
- Transformation steps include:
  - Removing duplicate or invalid records.
  - Converting timestamps into structured time dimensions (`dim_time`).
  - Standardizing cryptocurrency information into the `dim_coin` table.
  - Calculating and enriching key financial metrics such as `price_change_24h` and `market_cap` for storage in the `fact_coin_measurements` table.

**Load (Data Loading):**
- Processed data is inserted into a PostgreSQL database structured as a Star Schema:
  - `dim_coin` stores static cryptocurrency details.
  - `dim_time` captures time-based metadata (day, month, year, hour, etc.).
  - `fact_coin_measurements` stores market metrics linked to `dim_coin` and `dim_time` via foreign keys.
- Once loaded, the data is ready for querying, analysis, and visualization.

### 3. Data Visualization with Metabase
- **Metabase**: Used to build dashboards and visualize data from the Data Warehouse.
- **Supported Charts**:
  - **Line Chart**: Tracks metrics like `current_price` and `market_cap` over time.
  - **Bar Chart**: Compares cryptocurrencies at a specific point in time.
  - **Scatter Plot**: Analyzes relationships between different metrics.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/crypto-dwh-etl.git
cd crypto-dwh-etl
```

### 2. Configuration
- Modify configuration files, DDL scripts (`init_dw.sql`), or connection parameters for PostgreSQL and MinIO based on your environment.

### 3. Start Docker Compose
```bash
docker-compose up -d
```
This command starts containers for PostgreSQL, MinIO, and Metabase.

### 4. Run the ETL Pipeline
- The Python ETL script scans new CSV files on MinIO, processes data, and loads it into PostgreSQL using the Star Schema model.
- ETL scheduling can be managed via Airflow or Cron, depending on your setup.

### 5. Access Metabase
- Open [http://localhost:3000](http://localhost:3000) in your browser.
- Connect Metabase to the PostgreSQL database (`crypto`) and build dashboards as needed.

## Data Pipeline

![image](https://i.ibb.co/7jd8Ykg/ETL-process.png)

- **Data Collection**: Fetches real-time market data from CoinGecko API and stores it in MinIO as CSV files.
- **Processing & Storage**: Transforms and loads data into a PostgreSQL database.
- **Visualization**: Data is analyzed and displayed using Metabase.

## Usage

### Explore Raw Data
- View the latest cryptocurrency market data.

### Access Metabase
- Open [http://localhost:3000](http://localhost:3000).
- Default credentials: `admin` / `admin`.
- Connect to PostgreSQL and explore datasets.

## Visualizations

- **Price Trends**: Track `current_price` and `market_cap` over time.
- **Comparison**: Compare different cryptocurrencies at a given timestamp.
- **Relationships**: Analyze correlations between `volume` and `price change`.
- **Real-Time Dashboards**: Monitor market performance interactively.

## Conclusion
This project successfully automates the extraction, transformation, and loading of cryptocurrency market data into a structured Data Warehouse. With Metabase, users can interactively explore data and gain insights into market trends. The use of Docker Compose simplifies the deployment of PostgreSQL, MinIO, and Metabase, ensuring a streamlined setup.

## Future Direction
- Integrate additional data sources for broader market analysis.
- Implement machine learning for price trend forecasting.
- Enable real-time data streaming for instant updates.
- Enhance dashboards with more advanced analytics.

## Contact
For any questions or feedback, please reach out to [tmquang120202@gmail.com](mailto:tmquang120202@gmail.com).

