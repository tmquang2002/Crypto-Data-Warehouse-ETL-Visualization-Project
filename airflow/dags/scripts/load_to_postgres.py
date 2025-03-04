import psycopg2
import pandas as pd
from minio import Minio
from minio.error import S3Error
from datetime import datetime
import pytz

# Kết nối MinIO
minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Thông tin PostgreSQL
DB_CONFIG = {
    "host": "postgres",
    "port": "5432",
    "dbname": "crypto",
    "user": "airflow",
    "password": "airflow"
}

BUCKET_NAME = "coin-bucket"

def get_processed_files():
    """
    Lấy danh sách file đã xử lý từ PostgreSQL.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS processed_files (
                file_name TEXT PRIMARY KEY
            );
        """)
        conn.commit()
        cur.execute("SELECT file_name FROM processed_files;")
        processed_files = {row[0] for row in cur.fetchall()}
        cur.close()
        conn.close()
        return processed_files
    except Exception as e:
        print(f"[ERROR] Lỗi khi lấy danh sách file đã xử lý: {e}")
        return set()

def mark_file_as_processed(file_name):
    """
    Đánh dấu một file là đã xử lý trong PostgreSQL.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO processed_files (file_name) VALUES (%s) ON CONFLICT DO NOTHING;", (file_name,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Lỗi khi cập nhật danh sách file đã xử lý: {e}")

def download_from_minio(object_name):
    """
    Tải file từ MinIO về bộ nhớ và đọc thành DataFrame.
    """
    try:
        data = minio_client.get_object(BUCKET_NAME, object_name)
        df = pd.read_csv(data)
        print(f"[INFO] Đã tải file '{object_name}' từ MinIO")
        return df
    except S3Error as e:
        print(f"[ERROR] Lỗi khi tải file từ MinIO: {e}")
        return None

def get_or_create_dim_coin(cur, coin_id, symbol, name, image, total_supply, max_supply):
    """
    Kiểm tra xem coin đã tồn tại trong dim_coin chưa.
    Nếu chưa, chèn mới và trả về coin_key.
    """
    cur.execute("SELECT coin_key FROM dim_coin WHERE coin_id = %s;", (coin_id,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        cur.execute("""
            INSERT INTO dim_coin (coin_id, symbol, name, image, total_supply, max_supply)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING coin_key;
        """, (coin_id, symbol, name, image, total_supply, max_supply))
        coin_key = cur.fetchone()[0]
        return coin_key

def get_or_create_dim_time(cur, full_timestamp):
    """
    Kiểm tra xem timestamp đã tồn tại trong dim_time chưa.
    Nếu chưa, chèn mới và trả về time_key.
    """
    # full_timestamp là đối tượng datetime
    cur.execute("SELECT time_key FROM dim_time WHERE full_timestamp = %s;", (full_timestamp,))
    result = cur.fetchone()
    if result:
        return result[0]
    else:
        # Tách các thành phần thời gian
        date = full_timestamp.date()
        year = full_timestamp.year
        month = full_timestamp.month
        day = full_timestamp.day
        hour = full_timestamp.hour
        minute = full_timestamp.minute
        second = full_timestamp.second
        day_of_week = full_timestamp.strftime("%A")
        quarter = (month - 1) // 3 + 1
        cur.execute("""
            INSERT INTO dim_time (full_timestamp, date, year, month, day, hour, minute, second, day_of_week, quarter)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING time_key;
        """, (full_timestamp, date, year, month, day, hour, minute, second, day_of_week, quarter))
        time_key = cur.fetchone()[0]
        return time_key

def load_to_dwh(df):
    """
    Nạp dữ liệu từ DataFrame vào Data Warehouse theo mô hình Star Schema:
    - Cập nhật thông tin coin vào dim_coin.
    - Cập nhật thông tin thời gian vào dim_time.
    - Nạp số liệu đo lường vào fact_coin_measurements.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        record_count = 0

        for index, row in df.iterrows():
            # Xử lý thông tin coin (dim_coin)
            coin_id = row['id']
            symbol = row['symbol']
            name = row['name']
            image = row['image']
            total_supply = row.get('total_supply', None)
            max_supply = row.get('max_supply', None)

            coin_key = get_or_create_dim_coin(cur, coin_id, symbol, name, image, total_supply, max_supply)

            # Xử lý thông tin thời gian (dim_time)
            last_updated_str = row['last_updated']
            try:
                full_timestamp = pd.to_datetime(last_updated_str)
            except Exception as e:
                print(f"[ERROR] Không chuyển đổi được last_updated '{last_updated_str}': {e}")
                continue

            time_key = get_or_create_dim_time(cur, full_timestamp)

            # Nạp số liệu vào fact_coin_measurements
            cur.execute("""
                INSERT INTO fact_coin_measurements (
                    coin_key, time_key, current_price, market_cap, market_cap_rank,
                    fully_diluted_valuation, total_volume, high_24h, low_24h,
                    price_change_24h, price_change_percentage_24h, market_cap_change_24h,
                    market_cap_change_percentage_24h, circulating_supply, ath,
                    ath_change_percentage, atl, atl_change_percentage
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                coin_key,
                time_key,
                row['current_price'],
                row['market_cap'],
                row['market_cap_rank'],
                row['fully_diluted_valuation'],
                row['total_volume'],
                row['high_24h'],
                row['low_24h'],
                row['price_change_24h'],
                row['price_change_percentage_24h'],
                row['market_cap_change_24h'],
                row['market_cap_change_percentage_24h'],
                row['circulating_supply'],
                row['ath'],
                row['ath_change_percentage'],
                row['atl'],
                row['atl_change_percentage'],
            ))
            record_count += 1

        conn.commit()
        cur.close()
        conn.close()
        print(f"[INFO] Đã nạp {record_count} bản ghi vào Data Warehouse thành công.")
    except Exception as e:
        print(f"[ERROR] Lỗi khi nạp dữ liệu vào Data Warehouse: {e}")

def run_etl():
    """
    ETL: Chỉ xử lý các file mới từ MinIO theo cấu trúc phân vùng Year/Month/Day/time.csv.
    """
    try:
        processed_files = get_processed_files()
        objects = minio_client.list_objects(BUCKET_NAME, recursive=True)
        file_count = 0

        for obj in objects:
            object_name = obj.object_name
            if object_name.endswith(".csv") and object_name not in processed_files:
                df = download_from_minio(object_name)
                if df is not None:
                    load_to_dwh(df)
                    mark_file_as_processed(object_name)
                    file_count += 1

        print(f"[INFO] Quá trình ETL hoàn tất. Đã xử lý {file_count} file mới từ MinIO.")
    except Exception as e:
        print(f"[ERROR] Lỗi khi thực hiện ETL: {e}")

if __name__ == "__main__":
    run_etl()
