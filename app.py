from app import create_app
from app.config import Config, ENV_MODE
from app.helpers.logging_helper import logger

app = create_app()

# Log thông tin về môi trường hiện tại
logger.info(f"App dang chay o moi truong: {ENV_MODE}")

# Log thông tin kết nối cơ sở dữ liệu
logger.info(f"[DB] Using database at: {Config.DB_PATH}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
# Chạy ứng dụng Flask
# Lưu ý: Chỉ sử dụng debug=True trong môi trường phát triển
# Trong môi trường sản xuất, nên tắt debug mode và sử dụng một WSGI server như Gunicorn hoặc uWSGI
# Ví dụ: gunicorn -w 4 app:app
# Trong đó -w 4 là số worker processes, có thể điều chỉnh theo số CPU cores của server
# Để chạy ứng dụng, sử dụng lệnh: python app.py
# Đảm bảo đã cài đặt các thư viện cần thiết trong requirements.txt
# Ví dụ: pip install -r requirements.txt
# Để chạy ứng dụng, cần cài đặt Flask và các thư viện phụ thuộc khác
