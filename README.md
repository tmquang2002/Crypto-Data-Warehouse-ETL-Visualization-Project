# Crypto Data Warehouse ETL & Visualization Project
<img src="https://i.ibb.co/WWh7JHGS/aa.png" alt="NCHMF" width="500"/>


## Table of Contents

- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [Setup Instructions](#setup-instructions)
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
- **Docker Compose**: Orchestrates services like Airflow, PostgreSQL, MinIO, and Metabase.
- **Airflow (Optional)**: Automates and schedules ETL jobs.

## System Architecture

<img src="https://i.ibb.co/35sXshnq/img.png" alt="NCHMF" width="1000"/>


### 1. Data Collection
- **Data Source**: CoinGecko API providing information on cryptocurrencies like Bitcoin, Ethereum, USDC, Tether, Binance Coin, Ripple, Cardano, Dogecoin, Solana, and Tron.
- **Crawl & Extract**: A Python script fetches API data and saves it as CSV files.
- **Storage on MinIO**: CSV files are uploaded to MinIO with a time-based directory structure (e.g., `2025/02/28/10-10-14.csv`).

### 2. ETL & Data Warehouse Process

**Extract (Data Extraction):**

- The system fetches cryptocurrency market data from the CoinGecko API at scheduled intervals.
- Data is saved in CSV format and uploaded to MinIO for storage.

**Transform (Data Transformation):**

- The ETL pipeline scans MinIO for new CSV files and processes the raw data.
- Data transformation steps include:
  - Cleaning and handling missing or duplicate values.
  - Standardizing timestamps and aligning data with `dim_time`.
  - Mapping cryptocurrency information to `dim_coin`.
  - Calculating and structuring market-related metrics for `fact_coin_measurements`.

**Load (Data Loading):**

- Transformed data is inserted into a PostgreSQL database designed as a Star Schema:
  - `dim_coin`: Stores cryptocurrency details (e.g., name, symbol, category).
  - `dim_time`: Contains structured time metadata (e.g., date, hour, minute).
  - `fact_coin_measurements`: Stores daily price changes, market cap, and trade volume.
- The structured data is then used for querying and visualization in Metabase.

### 3. Data Visualization with Metabase

- **Metabase**: Used to build dashboards and visualize data from the Data Warehouse.
- **Supported Charts**:Line Chart, Bar Chart, Scatter Plot,...

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/tmquang2002/Crypto-Data-Warehouse-ETL-Visualization-Project.git
```

### 2. Configuration
- Modify configuration files, DDL scripts (`init.sql`), or connection parameters for PostgreSQL and MinIO based on your environment.

### 3. Start Docker Compose
```bash
docker-compose up -d
```
This command starts containers for Airflow, PostgreSQL, MinIO, and Metabase.

### 4. Run the ETL Pipeline
<img src="https://i.ibb.co/gL0QSCgk/airflow.png" alt="NCHMF" width="500"/>

- Access the Airflow web interface at [http://localhost:8080](http://localhost:8080) and log in with the default credentials (`airflow` / `airflow`).
- Activate the ETL DAG and trigger the job.
- The ETL process includes the following steps:
  1. **Crawl Data**: Fetch cryptocurrency market data from the CoinGecko API.
  2. **Load to MinIO**: Store the raw data as CSV files in MinIO.
  3. **Extract & Transform**: Scan MinIO for new CSV files, clean the data, and prepare it for storage.
  4. **Load to Data Warehouse**: Insert transformed data into PostgreSQL following the Star Schema model.


### 5. Access MinIO

- Open [http://localhost:9000](http://localhost:9000) in your browser.
- Default credentials:
  - **Access Key**: `minioadmin`
  - **Secret Key**: `minioadmin`
- Browse and manage stored CSV files.
<img src="https://i.ibb.co/7NgZ31zt/min-IO-pic.png" alt="NCHMF" width="700"/>

### 5. Access Metabase
- Open [http://localhost:3000](http://localhost:3000) in your browser.
- Default credentials: `admin` / `admin`.
- Connect Metabase to the PostgreSQL database (`crypto`) and build dashboards as needed.

## Visualizations

<img src="https://i.ibb.co/Pz9FDN24/dashboard-coin-data.png" alt="NCHMF" width="700"/>

The dashboard built in Metabase provides key insights into cryptocurrency market data, including:

- **Coin Data Table**: Displays `current_price`, `market_cap`, `total_volume`, and `price_change_24h` for major cryptocurrencies.
- **Price Trends & Market Volume**:
  - A **line chart** visualizes Bitcoin's `current_price` and `total_volume` over time.
  - Trends in `market_cap` are shown across different timestamps.
- **Market Cap Breakdown**:
  - A **pie chart** illustrates the market dominance of major cryptocurrencies.
- **Price Change Analysis**:
  - A **bar chart** compares the percentage price changes of different coins in the last 24 hours.


## Conclusion
This project successfully automates the extraction, transformation, and loading of cryptocurrency market data into a structured Data Warehouse. With Metabase, users can interactively explore data and gain insights into market trends. The use of Docker Compose simplifies the deployment of Airflow, PostgreSQL, MinIO, and Metabase, ensuring a streamlined setup.

## Future Direction
- Integrate additional data sources for broader market analysis.
- Implement machine learning for price trend forecasting.
- Enable real-time data streaming for instant updates.
- Enhance dashboards with more advanced analytics.

## Contact
For any questions or feedback, please reach out to [tmquang120202@gmail.com](mailto:tmquang120202@gmail.com).

