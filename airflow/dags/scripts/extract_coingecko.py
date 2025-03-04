import requests
import pandas as pd
import os
from minio import Minio
from datetime import datetime
import pytz

def fetch_top_coins(output_path="coin_data.csv"):
    """
    Gọi API CoinGecko để lấy thông tin 3 đồng coin,
    lưu dữ liệu vào file CSV (mặc định: coin_data.csv).
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,usd-coin,tether,binancecoin,ripple,cardano,dogecoin,solana,tron",
        "order": "market_cap_desc",
        "per_page": "100",
        "page": "1",
        "sparkline": "false"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"[extract_coingecko] Đã lưu dữ liệu vào file '{output_path}'")
    else:
        print("Có lỗi khi gọi API CoinGecko. Mã lỗi:", response.status_code)

def upload_to_minio(local_path, bucket_name, minio_client):
    """
    Upload file CSV từ local_path lên MinIO theo phân vùng Year/Month/Day/time.csv theo giờ Việt Nam.
    """
    # Lấy thời gian hiện tại theo múi giờ Việt Nam (UTC+7)
    vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now = datetime.now(vietnam_tz)

    year = now.year
    month = f"{now.month:02d}"  # Định dạng 2 chữ số
    day = f"{now.day:02d}"
    time = now.strftime("%H-%M-%S")  # Định dạng giờ-phút-giây

    # Tạo đường dẫn object trên MinIO theo phân vùng
    object_name = f"{year}/{month}/{day}/{time}.csv"

    # Upload file
    minio_client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=local_path,
        content_type="text/csv"
    )
    print(f"[upload_minio] Đã upload file '{local_path}' lên MinIO tại '{object_name}' (giờ VN)")

if __name__ == "__main__":
    # 1. Gọi hàm extract để lấy file CSV cục bộ
    fetch_top_coins("coin_data.csv")
    
    # 2. Kết nối MinIO
    minio_client = Minio(
        "minio:9000",             # Địa chỉ MinIO; nếu đang chạy trên Docker network, tên service là "minio"
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    bucket_name = "coin-bucket"

    # Kiểm tra xem bucket đã tồn tại chưa, nếu chưa tạo mới.
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' đã được tạo.")
    else:
        print(f"Bucket '{bucket_name}' đã tồn tại.")

    # 3. Upload file CSV lên MinIO theo phân vùng
    upload_to_minio("coin_data.csv", bucket_name, minio_client)
