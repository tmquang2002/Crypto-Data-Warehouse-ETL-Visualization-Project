-- Tạo bảng dim_coin
CREATE TABLE IF NOT EXISTS dim_coin (
    coin_key SERIAL PRIMARY KEY,
    coin_id VARCHAR(50) UNIQUE,
    symbol VARCHAR(10),
    name VARCHAR(50),
    image VARCHAR(255),
    total_supply DECIMAL(18,2),
    max_supply DECIMAL(18,2)
);

-- Tạo bảng dim_time
CREATE TABLE IF NOT EXISTS dim_time (
    time_key SERIAL PRIMARY KEY,
    full_timestamp TIMESTAMP,
    date DATE,
    year INT,
    month INT,
    day INT,
    hour INT,
    minute INT,
    second INT,
    day_of_week VARCHAR(10),
    quarter INT
);

-- Tạo bảng fact_coin_measurements
CREATE TABLE IF NOT EXISTS fact_coin_measurements (
    measurement_id SERIAL PRIMARY KEY,
    coin_key INT REFERENCES dim_coin(coin_key),
    time_key INT REFERENCES dim_time(time_key),
    current_price DECIMAL(18,8),
    market_cap BIGINT,
    market_cap_rank INT,
    fully_diluted_valuation BIGINT,
    total_volume DECIMAL(18,2),
    high_24h DECIMAL(18,8),
    low_24h DECIMAL(18,8),
    price_change_24h DECIMAL(18,8),
    price_change_percentage_24h DECIMAL(10,2),
    market_cap_change_24h DECIMAL(18,2),
    market_cap_change_percentage_24h DECIMAL(10,2),
    circulating_supply DECIMAL(18,2),
    ath DECIMAL(18,8),
    ath_change_percentage DECIMAL(10,2),
    atl DECIMAL(18,8),
    atl_change_percentage DECIMAL(10,2)
);
