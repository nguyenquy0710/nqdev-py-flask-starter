import secrets
import os
from dotenv import load_dotenv

# 📁 Xác định thư mục base, BASE_DIR trỏ về gốc project (chứa /app và /data)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 🔍 Ưu tiên .env.dev nếu có, ngược lại fallback sang .env
ENV_PATH = os.path.join(BASE_DIR, "..", ".env.test")
if not os.path.exists(ENV_PATH):
    ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(dotenv_path=ENV_PATH)


class Config:
    BASE_DIR = BASE_DIR
    # 🔐 Mã bí mật tĩnh cho test (không cần random)
    SECRET_KEY = "test-secret" or secrets.token_hex(16)

    # 🧪 SQLite in-memory (rất nhanh, không ghi ra file)
    DB_PATH = ":memory:"

    # 🌐 Cấu hình QuestDB – có thể mock nếu cần
    QUESTDB_INFLUXDB_HOST = os.getenv(
        "QUESTDB_INFLUXDB_HOST", "") or "localhost"  # Default: "localhost"
    # gửi line protocol qua TCP. Default: 9009
    QUESTDB_TCP_PORT = int(os.getenv("QUESTDB_TCP_PORT", "") or "9009")
    # REST API để query. Default: 9000
    QUESTDB_REST_PORT = int(os.getenv("QUESTDB_REST_PORT", "") or "9000")
    QUESTDB_REST_URL = os.getenv(
        "QUESTDB_REST_URL", "") or f"http://{QUESTDB_INFLUXDB_HOST}:{QUESTDB_REST_PORT}"
    QUESTDB_HTTP_USER = os.getenv("QUESTDB_HTTP_USER", "") or ""
    QUESTDB_HTTP_PASSWORD = os.getenv("QUESTDB_HTTP_PASSWORD", "") or ""

    # Cấu hình schedulers background
    ENABLE_AUTO_UPDATE = os.getenv(
        "ENABLE_AUTO_UPDATE", "false").lower() == 'true'

    # Cấu hình Zalo App
    ZALO_APP_ID = os.getenv("ZALO_APP_ID", "") or "APP_ID"
    ZALO_APP_SECRET = os.getenv("ZALO_APP_SECRET", "") or "APP_SECRET"
    ZALO_REDIRECT_URI = os.getenv("ZALO_REDIRECT_URI", "") or "REDIRECT_URI"
