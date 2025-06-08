import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from datetime import datetime

# ✅ Load .env nếu tồn tại
load_dotenv()

# Ưu tiên lấy từ biến môi trường, mặc định là "dev"
ENV_MODE = os.getenv("APP_ENV", "dev")

if ENV_MODE == "prod":
    from .config_prod import Config
elif ENV_MODE == "test":
    from .config_test import Config
else:
    from .config_dev import Config

# Cấu hình thư mục logs trong BASE_DIR
# Dùng BASE_DIR hoặc mặc định là thư mục gốc
log_dir = os.path.join(Config.BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)  # Nếu thư mục logs không tồn tại, tạo mới

# Tạo đường dẫn file log
# Lấy ngày hiện tại và tạo tên file log theo ngày
# app-YYYY-MM-DD.log
log_file_name = f"app-{datetime.now().strftime('%Y-%m-%d')}.log"
log_file = os.path.join(log_dir, log_file_name)

# Cấu hình RotatingFileHandler để log không bị quá lớn (ví dụ: 10MB cho mỗi file)
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10 * 1024 * 1024,  # Kích thước tối đa 10MB
    backupCount=5,  # Giới hạn lưu tối đa 5 file log cũ
    encoding='utf-8'  # Đảm bảo file log sử dụng mã hóa UTF-8
)

# Cấu hình console handler với UTF-8 encoding
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))

# Đảm bảo console handler sử dụng mã hóa UTF-8
console_handler.encoding = 'utf-8'


# Cấu hình logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        file_handler,       # Ghi log vào file app.log trong thư mục logs
        console_handler,    # Ghi log ra console
    ]
)


# Lấy logger toàn cục
logger = logging.getLogger(__name__)

# Log thông tin về môi trường hiện tại
logger.info(f"App dang chay o moi truong: {ENV_MODE}")

# Log thông tin kết nối cơ sở dữ liệu
logger.info(f"[DB] Using database at: {Config.DB_PATH}")

# Function to log HTTP access


def log_http_access(request_method, request_path, response_status):
    logger.info(
        f"[HTTP] {request_method} {request_path} - Status: {response_status}")

# Example usage of log_http_access
# log_http_access('GET', '/api/v1/resource', 200)
