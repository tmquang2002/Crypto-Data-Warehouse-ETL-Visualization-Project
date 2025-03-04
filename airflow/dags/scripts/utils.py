import os
import json

def get_db_config():
    """
    Lấy config DB từ biến môi trường (hoặc file .env).
    Trả về dict cho psycopg2.
    """
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": os.getenv("DB_NAME", "crypto"),
        "user": os.getenv("DB_USER", "airflow"),
        "password": os.getenv("DB_PASSWORD", "airflow"),
    }

def upload_to_minio(file_path, minio_client, bucket_name):
    """
    Hàm upload file lên MinIO, ví dụ sử dụng minio-py
    """
    # from minio import Minio
    # ...
    pass
